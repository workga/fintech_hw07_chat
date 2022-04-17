from pydantic import BaseSettings


class AppSettings(BaseSettings):
    logger_name: str
    logger_level: str

    redis_host: str
    redis_port: int

    class Config:
        env_file = 'app/.env'
        env_file_encoding = 'utf-8'


app_settings = AppSettings()
