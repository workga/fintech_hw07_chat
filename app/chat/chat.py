import asyncio
from ssl import CHANNEL_BINDING_TYPES

from fastapi.websockets import WebSocket, WebSocketDisconnect
from redis import Redis, RedisError
from starlette.websockets import WebSocketState

from app.redis_db import redis_connection
from app.logger import logger
from app.chat.settings import chat_settings



active_users = set()

    
def validate_message(message: str):
    return message.startswith('@') and ' ' in message


def encode_channel(user_id: str):
    return f'channel_{user_id}'


def encode_history_list(user_id: str):
    return f'history_list_{user_id}'


def encode_messsage(message: str, user_id: str):
    return f'@{user_id} {message}'


def decode_message(message: str):
    dest_user_id, message = message[1:].split(' ', 1)
    return dest_user_id, message


async def send(ws: WebSocket, user_id: str):
    try:
        channel = encode_channel(user_id)

        with redis_connection() as conn:
            pubsub = conn.pubsub()
            await pubsub.subscribe(channel)
            
            async for message in pubsub.listen():
                if message['type'] == 'message':
                    await ws.send_bytes(message['data'])

            pubsub.unsubscribe(channel)
    except WebSocketDisconnect:
        return
    except RedisError:
        return


async def receive(ws: WebSocket, user_id: str):
    try:
        while ws.client_state == WebSocketState.CONNECTED:
            raw_message = await ws.receive_text()

            if not validate_message(raw_message):
                await ws.send_text('ERROR: Invalid message')
                continue

            dest_user_id, message = decode_message(raw_message)

            if dest_user_id not in active_users:
                await ws.send_text('ERROR: User is not active')
                continue

            channel = encode_channel(dest_user_id)
            history_list = encode_history_list(dest_user_id)
            message = encode_messsage(message, user_id)

            with redis_connection() as conn:
                await conn.publish(channel, message)
                await conn.lpush(history_list, message)

    except WebSocketDisconnect:
        return
    except RedisError:
        return


async def handle_ws_connection(ws: WebSocket, user_id: str):
    await ws.accept()

    if user_id in active_users:
        await ws.send_text('ERROR: User is already active')
        await ws.close()

        logger.info(f'Unavailable user_id: {user_id}')
        return

    active_users.add(user_id)
    logger.info(f'Connected: {user_id}')


    send_task = asyncio.create_task(send(ws, user_id))
    receive_task = asyncio.create_task(receive(ws, user_id))

    _, pending = await asyncio.wait(
        [send_task, receive_task],
        return_when=asyncio.FIRST_COMPLETED,
    )

    for task in pending:
        task.cancel()

    active_users.remove(user_id)

    logger.info(f'Disconnected: {user_id}')


async def get_history(user_id: str):
    history_list = encode_history_list(user_id)

    with redis_connection() as conn:
        messages = await conn.lrange(
            history_list,
            0,
            chat_settings.history_length - 1
        )

    return messages
