from typing import List
from pydantic import BaseSettings, Field
import os
import logging
from logging.handlers import RotatingFileHandler
import inspect


def get_database_url():
    return f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"


class Config(BaseSettings):
    DATABASE_URL: str = Field(...)
    ALLOWED_ORIGINS: List = Field(...)
    SECRET_KEY: str = Field(...)
    API_KEY: str = Field(...)


class Logger:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.set_level()
        self.create_handlers()

    def set_level(self):
        self.logger.setLevel(logging.INFO)

    def get_formatter(self):
        return logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

    def create_handlers(self):
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self.get_formatter())

        file_handler = RotatingFileHandler(
            "logs/api_logs.log", maxBytes=10 * 1024 * 1024, backupCount=3
        )
        file_handler.setFormatter(self.get_formatter())

        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)


config_instance = Config(
    DATABASE_URL=get_database_url(),
    ALLOWED_ORIGINS=["http://localhost:8080"],
    API_KEY=os.getenv("API_KEY") or "__INVALID_API_KEY__",
    SECRET_KEY=os.getenv("SECRET_KEY") or "__INVALID_SECRET_KEY__",
)

logging_instance = Logger().logger


def log_sql(query):
    caller_name = inspect.stack()[1].function
    logging_instance.info(f"{caller_name} -> {str(query)}")
