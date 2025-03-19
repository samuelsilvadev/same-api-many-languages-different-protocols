from pydantic import BaseSettings, Field
import os


def get_database_url():
    return f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"


class Config(BaseSettings):
    DATABASE_URL: str = Field(...)


config_instance = Config(DATABASE_URL=get_database_url())
