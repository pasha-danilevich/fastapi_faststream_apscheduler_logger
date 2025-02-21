import os
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic_settings import SettingsConfigDict, BaseSettings

BASE_PATH = Path(__file__).parent


class Base(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_PATH, ".env"),
        env_file_encoding="utf-8",
        # env_ignore_empty=True,
        extra="ignore",
    )


class Redis(Base):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_STORE_DB_INDEX: int
    REDIS_PASSWORD: str


class RabbitMQ(Base):
    RABBITMQ_HOST: str
    RABBITMQ_USER: str
    RABBITMQ_PASS: str
    RABBITMQ_PORT: int


class Log(Base):

    LOG_LEVEL: str = "INFO"

    LOG_MODE: Literal["DEV", "PROD"] = "DEV"

    LOG_INCLUDE_PACKAGES: list[str]  # если пустой, то все пакеты логгируются
    LOG_INCLUDE_MODULES: list[str]

    LOG_EXCLUDE_PACKAGES: list[str]
    LOG_EXCLUDE_MODULES: list[str]


class Settings(RabbitMQ, Redis, Log):
    pass


@lru_cache()
def get_settings():
    return Settings()


settings: Settings = get_settings()
