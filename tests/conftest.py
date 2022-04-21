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
    return mocker.patch('app.redis_db.redis.Redis', spec=True)
