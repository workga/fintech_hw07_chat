import asyncio

import pytest


def test_send_receive_success(mocker, client, mocked_redis, mocked_pubsub):
    sender_id = 'annet'
    receiver_id = 'bella'
    sent_messages = [
        '@bella hi',
        '@clare hi',
        '@bella bye',
        '@clare bye',
    ]
    stored_messages = [
        {
            'type': 'message',
            'data': '@bella hi',
        },
        {
            'type': 'message',
            'data': '@bella bye',
        },
    ]
    received_messages = [
        '@bella hi',
        '@bella bye',
    ]

    async def message_generator():
        for message in stored_messages:
            yield message
        yield await asyncio.sleep(2)

    mocked_pubsub.listen = message_generator

    # I mock 'active_users' because I can't keep both websocket connections simultaneously
    mocker.patch('app.chat.chat.active_users', {'bella', 'clare'})
    with client.websocket_connect(f'/chat/{sender_id}/ws') as sender_ws:
        for message in sent_messages:
            sender_ws.send_text(message)

    mocker.patch('app.chat.chat.active_users', set())
    with client.websocket_connect(f'/chat/{receiver_id}/ws') as receiver_ws:
        result = []
        for _ in range(len(received_messages)):
            result.append(receiver_ws.receive_text())

    assert result == received_messages
    assert mocked_redis.publish.call_count == len(sent_messages)
    assert mocked_redis.lpush.call_count == len(sent_messages)


@pytest.mark.asyncio
async def test_receive_fail_unavailable_user_error(
    mocker, client, mocked_pubsub, listen_generator
):
    sender_id = 'annet'
    sent_message = '@bella hi'

    mocked_pubsub.listen = listen_generator

    mocker.patch('app.chat.chat.active_users', set())
    with client.websocket_connect(f'/chat/{sender_id}/ws') as sender_ws:
        sender_ws.send_text(sent_message)
        response = sender_ws.receive_text()

    assert response == 'ERROR: User is not active'


@pytest.mark.asyncio
async def test_receive_fail_user_already_active_error(
    mocker, client, mocked_pubsub, listen_generator
):
    sender_id = 'annet'

    mocked_pubsub.listen = listen_generator

    mocker.patch('app.chat.chat.active_users', {'annet'})
    with client.websocket_connect(f'/chat/{sender_id}/ws') as sender_ws:
        response = sender_ws.receive_text()

    assert response == 'ERROR: User is already active'


@pytest.mark.parametrize(
    'sent_message',
    [
        'bella hi',
        '@bella',
        'bella',
    ],
)
@pytest.mark.asyncio
async def test_receive_fail_invalid_message_error(
    mocker, client, sent_message, mocked_pubsub, listen_generator
):
    sender_id = 'annet'

    mocked_pubsub.listen = listen_generator

    mocker.patch('app.chat.chat.active_users', set())
    with client.websocket_connect(f'/chat/{sender_id}/ws') as sender_ws:
        sender_ws.send_text(sent_message)
        response = sender_ws.receive_text()

    assert response == 'ERROR: Invalid message'