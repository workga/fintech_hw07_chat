from functools import wraps
from typing import Any, Callable, TypeVar, cast

import redis
from redis.exceptions import RedisError

from app.logger import logger
from app.settings import app_settings

F = TypeVar('F', bound=Callable[..., Any])

connection_pool = redis.ConnectionPool(
    host=app_settings.redis_host,
    port=app_settings.redis_port,
    db=0,
)


def redis_connection(func: F) -> F:
    @wraps(func)
    def wrapper(*args: int, **kwargs: int) -> Any:
        try:
            conn = redis.Redis(connection_pool=connection_pool)
            return func(*args, conn=conn, **kwargs)
        except RedisError as error:
            logger.error(error)
            raise

    return cast(F, wrapper)
