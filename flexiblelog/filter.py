import inspect
import logging
from pathlib import Path

from flexiblelog.exceptions import PackageNotFound

from flexiblelog.record import CustomLogRecord
from flexiblelog.schemas import FilterType


# TODO вынести данный класс в formatter
class FuncArgsFilter(logging.Filter):
    def filter(self, record: CustomLogRecord) -> bool:
        # Получаем текущий фрейм (стек вызовов)
        frame = inspect.currentframe()
        try:
            # Идем по стеку вызовов, чтобы найти фрейм функции, которая вызвала логгер
            while frame:
                # Проверяем, что это фрейм функции, а не логгера
                if frame.f_code.co_name == record.funcName:
                    # Получаем аргументы функции из фрейма
                    args, _, _, values = inspect.getargvalues(frame)
                    if args:  # Если есть аргументы
                        # Формируем список аргументов в виде dict[str, any]
                        record.func_args = {arg: values[arg] for arg in args}
                        break
                frame = frame.f_back  # Переходим к предыдущему фрейму
        finally:
            del frame  # Удаляем фрейм, чтобы избежать утечек памяти

        return True  # Всегда пропускаем запись


class FilterPackages(logging.Filter):

    def __init__(self, user_packages, packages, filter_type: FilterType, base_path: Path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_path = base_path
        self.is_can_log = True if filter_type == FilterType.ONLY else False
        self.packages = packages

    def filter(self, record: CustomLogRecord) -> bool:
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
    def filter(self, record: CustomLogRecord) -> bool:
        # absolute_path = Path(record.pathname)
        # relative_path = absolute_path.relative_to(BASE_PATH)
        return True
        # if record.msg != 'error':
        #     return True
        # else:
        #     return False
