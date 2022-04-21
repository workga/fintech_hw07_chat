import asyncio
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.app import create_app


@pytest.fixture(name='app')
def fixture_app():
    return create_app()


@pytest.fixture(name='client')
def fixture_client(app):
    return TestClient(app)


@pytest.fixture(name='mocked_redis', autouse=True)
def fixture_mocked_redis(mocker):
    mocked_redis = mocker.patch('app.redis_db.Redis', spec=True).return_value

    mocked_redis.publish = AsyncMock(return_value=None)
    mocked_redis.lpush = AsyncMock(return_value=None)

    return mocked_redis


@pytest.fixture(name='mocked_pubsub', autouse=True)
def fixture_mocked_pubsub(mocked_redis):
    mocked_pubsub = mocked_redis.pubsub.return_value

    mocked_pubsub.subscribe = AsyncMock(return_value=None)
    mocked_pubsub.unsubscribe = AsyncMock(return_value=None)

    return mocked_pubsub


@pytest.fixture(name='listen_generator')
def fixture_listen_generator():
    async def message_generator():
        yield await asyncio.sleep(2)

    return message_generator
