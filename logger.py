import logging

from flexiblelog import LoggerSettings, create_logger
from settings import settings, BASE_PATH

logger_settings = LoggerSettings(
    LOGGER_NAME=settings.LOGGER_NAME,
    LEVEL=settings.LOG_LEVEL,
    MODE=settings.LOG_MODE,
    PACKAGES_FILTER_TYPE=settings.LOG_PACKAGES_FILTER_TYPE,
    PACKAGES=settings.LOG_PACKAGES,
    MODULES_FILTER_TYPE=settings.LOG_MODULES_FILTER_TYPE,
    MODULES=settings.LOG_MODULES,
)


logger = create_logger(base_path=BASE_PATH, settings=logger_settings)

# s_logger = logging.getLogger("flexiblelog")
# a = s_logger.findCaller(True, 1)