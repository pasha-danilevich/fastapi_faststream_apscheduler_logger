import os
from enum import Enum
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


class FilterType(str, Enum):
    ONLY: str = "ONLY"
    WITHOUT: str = "WITHOUT"

class Log(Base):
    """
     LOG_PACKAGES/MODULES='' - включены все, если ничего не передавать.
     В не зависимости от LOG_PACKAGES/MODULES_RULE

    ---

    Список пакетов и модулей перечислить через запятую с пробелом.
    Пример:
    LOG_PACKAGES/MODULES='name, name, name'

    ---

    Если необходимо включить/исключить вложенный пакет,
    необходимо прописать через точку родительские пакеты.
    Пример:
    LOG_PACKAGES='name, name.in_some, name.in_some.some_some'

    ---

    Logger сперва включает пакеты/модули затем исключает
    Пример:
    LOG_PACKAGES_RULE='INCLUDE'
    LOG_PACKAGES='api, models, test'

    LOG_MODULES_RULE='EXCLUDE'
    LOG_MODULES='test_file.py'
    Итог: логгированию подлежат пакеты: api, models и все модули в пакете test кроме test_file.py

    ---

    Более высокая иерархия перекроет низшую пакетов.
    Пример:
    LOG_PACKAGES_RULE='INCLUDE'
    LOG_PACKAGES='api.v2, bg, service, api, api.service, bg.routers, api.service.v1'
    Итог: логгированию подлежат пакеты (bg, service, api)

    ---

    Если хотите включить/исключить все модули, находящиеся в корне проекта
    (модули, не находящиеся в каком-либо пакете), добавьте "root"
    в LOG_PACKAGES
    """

    LOGGER_NAME: str = "promed-service"

    LOG_LEVEL: str = "INFO"

    LOG_MODE: Literal["DEV", "PROD"] = "DEV"

    LOG_PACKAGES_FILTER_TYPE: Literal[FilterType.ONLY, FilterType.WITHOUT] = "ONLY"
    LOG_PACKAGES: str = ''

    LOG_MODULES_FILTER_TYPE: Literal[FilterType.ONLY, FilterType.WITHOUT] = "ONLY"
    LOG_MODULES: str = ''


class Settings(RabbitMQ, Redis, Log):
    pass


@lru_cache()
def get_settings():
    return Settings()


settings: Settings = get_settings()
