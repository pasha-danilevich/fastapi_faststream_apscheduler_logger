# flexiblelog/builder.py
import logging

from pathlib import Path
from typing import Set, Type

from flexiblelog.packages import PackageList
from flexiblelog.schemas import LoggerSettings

from flexiblelog.filter import FuncArgsFilter, FilterPackages, FilterModules
from flexiblelog.formatter import ColourFormatter
from flexiblelog.record import custom_log_record_factory


# from flexiblelog.utils import clear_empty_item


# ссылка 1
# def get_sql_file(file_name=None):
#     path = os.path.dirname(__file__)
#     result = [
#         os.path.join(root, f)
#         for root, dirs, filenames in os.walk(path)
#         for f in filenames
#         if os.path.basename(f) == file_name
#     ]
#     return result[0]


class LoggerBuilder:
    def __init__(
            self,
            base_path: Path,
            settings: LoggerSettings,
            formatter_class: Type[logging.Formatter] = ColourFormatter,

    ) -> None:
        self.stt: LoggerSettings = settings
        self.formatter_class = formatter_class
        self.base_path = base_path

        self.packages_filter_type = self.stt.PACKAGES_FILTER_TYPE
        self.packages_list_obj = PackageList(base_path, self.stt.PACKAGES)
        self.packages_list = self.packages_list_obj.packages

        # ссылка 1 для модулей
        self.modules_filter_type = self.stt.MODULES_FILTER_TYPE
        self.modules_list: Set[str] = set(
            self.stt.MODULES.split(', ')
        )

    def build(self) -> logging.Logger:
        """Создает и настраивает логгер."""
        # Создаем обработчик для вывода в консоль
        console_handler = logging.StreamHandler()

        # Устанавливаем фабрику для создания пользовательских записей логов
        logging.setLogRecordFactory(custom_log_record_factory)

        # Добавляем фильтры
        console_handler.addFilter(FuncArgsFilter())
        console_handler.addFilter(
            FilterPackages(
                self.packages_list, self.packages_list, self.packages_filter_type, self.base_path
            )
        )
        console_handler.addFilter(FilterModules())

        # Настраиваем форматтер
        console_handler.setFormatter(self.formatter_class())

        # Создаем логгер и настраиваем его
        logger = logging.getLogger(self.stt.LOGGER_NAME)
        logger.setLevel(self.stt.LEVEL)
        logger.addHandler(console_handler)

        return logger

    def __str__(self):
        return (
                (
                        f'Установленны фильтры: \n'
                        f"Packages: "
                        + (
                            f'{self.packages_filter_type.value}: {self.packages_list_obj}'
                            if self.packages_list
                            else "ALL"
                        )
                )
                + ' | '
                + (
                        f"Modules: "
                        + (
                            f'{self.modules_filter_type.value}: {self.stt.MODULES.split(", ")}'
                            if self.modules_list
                            else "ALL"
                        )
                )
        )
