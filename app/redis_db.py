from contextlib import contextmanager

from redis.asyncio.client import Redis
from redis.asyncio.connection import ConnectionPool
from redis.exceptions import RedisError

from app.logger import logger
from app.settings import app_settings

connection_pool = ConnectionPool(
    host=app_settings.redis_host,
    port=app_settings.redis_port,
    db=0,
)


@contextmanager
def redis_connection() -> Redis:
    try:
        yield Redis(connection_pool=connection_pool)
    except RedisError as error:
        logger.error(error)
        raise
