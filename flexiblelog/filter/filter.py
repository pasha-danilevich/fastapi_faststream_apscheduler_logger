import logging
from pathlib import Path
from sys import modules

from flexiblelog.schemas import FilterType




class FilterPackages(logging.Filter):

    def __init__(self, packages, filter_type: FilterType, base_path: Path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_path = base_path
        self.is_can_log = True if filter_type == FilterType.ONLY else False
        self.packages = packages

    def filter(self, record: logging.LogRecord) -> bool:
        # Если пакеты для фильтрации не заданы, пропускаем все записи
        if not self.packages:
            return True

        relative_path = self.get_relative_path(record)

        if not self._is_package(relative_path):
            if 'root' in self.packages:
                return self.is_can_log

        for package in self.packages:

            if relative_path.startswith(package):
                return self.is_can_log
            else:
                continue
        else:
            return not self.is_can_log


    def get_relative_path(self, record: logging.LogRecord) -> str:
        absolute_path = Path(record.pathname)
        return str(absolute_path.relative_to(self.base_path))


    @staticmethod
    def _is_package(relative_path: str) -> bool:
        """Проверяем, содержит ли путь хотя бы один пакет (например, есть ли в пути '/')"""
        return '/' in relative_path





class FilterModules(logging.Filter):
    def __init__(self, modules, filter_type: FilterType, base_path: Path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_path = base_path
        self.is_can_log = True if filter_type == FilterType.ONLY else False
        self.modules = modules

    def filter(self, record: logging.LogRecord) -> bool:

        if not self.modules:
            return True

        relative_path = self.get_relative_path(record)

        for modul in self.modules:

            len_ = len(modul.split('/'))
            arr_path = relative_path.split('/')[-len_:]

            if '/'.join(arr_path) == modul:
                return self.is_can_log
            else:
                continue
        else:
            return not self.is_can_log

    def get_relative_path(self, record: logging.LogRecord) -> str:
        absolute_path = Path(record.pathname)
        return str(absolute_path.relative_to(self.base_path))


