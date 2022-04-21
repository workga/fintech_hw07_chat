import asyncio

import requests
import typer
import websockets
from websockets.exceptions import WebSocketException
from websockets.legacy.client import WebSocketClientProtocol as WebSocket

from client.settings import client_settings


def echo_history(user_id: str) -> None:
    hist_url = (
        f'http://{client_settings.host}:{client_settings.port}/chat/{user_id}/history'
    )

    response = requests.get(hist_url)

    if response.status_code != 200:
        return

    history_list = response.json()
    for message in history_list:
        typer.echo(message)


async def async_input() -> str:
    return await asyncio.get_event_loop().run_in_executor(None, input)


async def send(ws: WebSocket) -> None:
    try:
        while message := await async_input():
            await ws.send(message)

    except WebSocketException as error:
        typer.echo(f'ERROR: {error}')
        return


async def receive(ws: WebSocket) -> None:
    try:
        async for message in ws:
            typer.echo(message)

    except WebSocketException as error:
        typer.echo(f'ERROR: {error}')


async def client(user_id: str) -> None:
    try:
        ws_url = f'ws://{client_settings.host}:{client_settings.port}/chat/{user_id}/ws'
        typer.echo(f'INFO: Connecting to {ws_url}')

        # Because pylint doesn't know about connect method
        async with websockets.connect(  # type: ignore[attr-defined]  # pylint: disable=no-member
            ws_url
        ) as ws:
            typer.echo('INFO: Connected')

            echo_history(user_id)

            send_task = asyncio.create_task(send(ws))
            receive_task = asyncio.create_task(receive(ws))

            _, pending = await asyncio.wait(
                [send_task, receive_task],
                return_when=asyncio.FIRST_COMPLETED,
            )

            await ws.close()

            for task in pending:
                task.cancel()

            typer.echo('INFO: Disconnected')
    except (requests.exceptions.ConnectionError, ConnectionRefusedError):
        typer.echo('ERROR: Connection error')


def main(user_id: str) -> None:
    asyncio.run(client(user_id))


if __name__ == '__main__':
    typer.run(main)
