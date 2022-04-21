from pydantic import BaseSettings


class ClientSettings(BaseSettings):
    host: str
    port: int

    class Config:
        env_file = 'client/.env'
        env_file_encoding = 'utf-8'


client_settings = ClientSettings()
