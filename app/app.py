from fastapi import FastAPI, Request, Response
from redis.exceptions import RedisError

from app.chat.routes import router as chat_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(chat_router, prefix='/chat')

    # Because this decorator needs a function with such arguments
    @app.exception_handler(RedisError)
    def handle_db_exceptions(
        request: Request, exception: RedisError  # pylint: disable=unused-argument
    ) -> Response:
        return Response(status_code=500)

    return app
