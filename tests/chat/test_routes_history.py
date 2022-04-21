from unittest.mock import AsyncMock

from redis.exceptions import RedisError


def test_get_success(client, mocked_redis):
    user_id = 'annet'
    history_list = [
        '@bella hello',
        '@clare hello',
    ]

    mocked_redis.lrange = AsyncMock(return_value=history_list)

    response = client.get(f'/chat/{user_id}/history')

    assert response.status_code == 200

    data = response.json()
    assert data == history_list


def test_get_fail_db_error(client, mocked_redis):
    user_id = 'annet'

    mocked_redis.lrange = AsyncMock(side_effect=RedisError)

    response = client.get(f'/chat/{user_id}/history')

    assert response.status_code == 500
