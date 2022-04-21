from pydantic import BaseSettings


class ChatSettings(BaseSettings):
    history_length: int

    class Config:
        env_file = 'app/chat/.env'
        env_file_encoding = 'utf-8'


chat_settings = ChatSettings()
