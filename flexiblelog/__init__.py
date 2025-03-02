# flexiblelog/__init__.py
from logging import Formatter
from pathlib import Path
from typing import Type

from flexiblelog.builder import LoggerBuilder
from flexiblelog.formatter import LogFormatter
from flexiblelog.schemas import LoggerSettings

# Фабричная функция для создания логгера
def create_logger(
        base_path: Path,
        settings: LoggerSettings,
        formatter_class: Type[Formatter] = LogFormatter,
):
    logger_builder = LoggerBuilder(
        base_path=base_path,
        settings=settings,
        formatter_class=formatter_class,
    )

    logger = logger_builder.build()
    logger.info(logger_builder)
    return logger
