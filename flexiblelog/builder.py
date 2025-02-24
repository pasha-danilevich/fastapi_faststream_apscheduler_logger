# flexiblelog/builder.py
import logging
import os

from pathlib import Path
from typing import Set, Type

from flexiblelog.folders import ProjectFolders
from flexiblelog.schemas import LoggerSettings, FilterType
from flexiblelog.utils import clear_empty_item, subtract_sets

from flexiblelog.filter import FuncArgsFilter, FilterPackages, FilterModules
from flexiblelog.formatter import ColourFormatter
from flexiblelog.record import custom_log_record_factory


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
        self.packages_list = self._get_packages_list()

        # ссылка 1 для модулей
        self.modules_filter_type = self.stt.MODULES_FILTER_TYPE
        self.modules_list: Set[str] = set(clear_empty_item(self.stt.MODULES.split(', ')))

    def _get_packages_list(self) -> Set[str]:
        packages_list: Set[str] = set(clear_empty_item(self.stt.PACKAGES.split(', ')))

        if self.packages_filter_type == FilterType.WITHOUT.value:
            all_folders = self._get_all_project_folders()
            packages_list = subtract_sets(all_folders, packages_list)

        return packages_list

    # TODO данная логика должна быть у ProjectFolders
    def _get_all_project_folders(self) -> Set[str]:
        gitignore_path = os.path.join(self.base_path, ".gitignore")
        project_folders = ProjectFolders(self.base_path, gitignore_path)
        all_folders: Set[str] = project_folders.get_folders()
        all_folders.add('root')  # Корневая папка проекта
        return all_folders

    def build(self) -> logging.Logger:
        """Создает и настраивает логгер."""
        # Создаем обработчик для вывода в консоль
        console_handler = logging.StreamHandler()

        # Устанавливаем фабрику для создания пользовательских записей логов
        logging.setLogRecordFactory(custom_log_record_factory)

        # Добавляем фильтры
        console_handler.addFilter(FuncArgsFilter())
        console_handler.addFilter(FilterPackages(self.packages_list, self.packages_filter_type, self.base_path))
        console_handler.addFilter(FilterModules())

        # Настраиваем форматтер
        console_handler.setFormatter(self.formatter_class())

        # Создаем логгер и настраиваем его
        logger = logging.getLogger(self.stt.LOGGER_NAME)
        logger.setLevel(self.stt.LEVEL)
        logger.addHandler(console_handler)

        return logger

    def __str__(self):
        return ((f'logging {self.packages_filter_type.value}: {self.stt.PACKAGES.split(", ")} packages'
                 if self.packages_list else 'Logging ALL packages')
                + ' and ' +
                (f'{self.modules_filter_type.value}: {self.stt.MODULES.split(", ")} modules'
                 if self.modules_list else 'ALL modules'))
