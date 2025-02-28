import logging
from pathlib import Path

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


        absolute_path = Path(record.pathname)
        relative_path = str(absolute_path.relative_to(self.base_path))

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



    @staticmethod
    def _is_package(relative_path: str) -> bool:
        """Проверяем, содержит ли путь хотя бы один пакет (например, есть ли в пути '/')"""
        return '/' in relative_path





class FilterModules(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        # absolute_path = Path(record.pathname)
        # relative_path = absolute_path.relative_to(BASE_PATH)
        return True
        # if record.msg != 'error':
        #     return True
        # else:
        #     return False
