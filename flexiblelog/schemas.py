# flexiblelog/schemas.py
from enum import Enum
from typing import Literal

from pydantic import BaseModel


class FilterType(str, Enum):
    ONLY: str = "ONLY"
    WITHOUT: str = "WITHOUT"

class LoggerSettings(BaseModel):
    LOGGER_NAME: str = "promed-service"

    LEVEL: str = "INFO"
    # TODO: rename to ENV
    MODE: Literal["DEV", "PROD"] = "DEV"

    PACKAGES_FILTER_TYPE: Literal[FilterType.ONLY, FilterType.WITHOUT] = "ONLY"
    PACKAGES: str = ''

    MODULES_FILTER_TYPE: Literal[FilterType.ONLY, FilterType.WITHOUT] = "ONLY"
    MODULES: str = ''

    USE_PID: bool = False