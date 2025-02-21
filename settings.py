import os
from typing import Literal

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict





class Settings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_STORE_DB_INDEX: int
    REDIS_PASSWORD: str

    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_USER: str = "motodokt"
    RABBITMQ_PASS: str = "motodokt"
    RABBITMQ_PORT: int = 5672

    LOG_MODE: Literal["DEV", "PROD"] = "DEV"

    LOG_LEVEL: str = "INFO"

    LOG_INCLUDE_PACKAGES: list[str] = [] # если пустой, то все пакеты логгируются
    LOG_INCLUDE_MODULES: list[str] = []

    LOG_EXCLUDE_PACKAGES: list[str] = []
    LOG_EXCLUDE_MODULES: list[str] = []

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    )




settings = Settings()