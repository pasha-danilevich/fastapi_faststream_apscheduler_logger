# flexiblelog/schemas.py
from enum import Enum
from typing import Literal
from fastapi import Header
from pydantic import BaseModel, field_validator


class FilterType(str, Enum):
    ONLY: str = "ONLY"
    WITHOUT: str = "WITHOUT"

class LoggerSettings(BaseModel):
    LOGGER_NAME: str = "promed-service"

    LEVEL: str = "INFO"

    MODE: Literal["DEV", "PROD"] = "DEV"

    PACKAGES_FILTER_TYPE: Literal[FilterType.ONLY, FilterType.WITHOUT] = "ONLY"
    PACKAGES: str = ''

    MODULES_FILTER_TYPE: Literal[FilterType.ONLY, FilterType.WITHOUT] = "ONLY"
    MODULES: str = ''

    USE_PID: bool = False