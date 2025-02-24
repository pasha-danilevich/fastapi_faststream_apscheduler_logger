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

    def __init__(self, packages, filter_type: FilterType, base_path: Path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_path = base_path

        self._check_exists_path(packages)
        self.packages = packages if filter_type.value == "WITHOUT" else self._remove_substrings(packages)


    def filter(self, record: CustomLogRecord) -> bool:
        # Если пакеты для фильтрации не заданы, пропускаем все записи
        if not self.packages:
            return True

        absolute_path = Path(record.pathname)
        relative_path = str(absolute_path.relative_to(self.base_path))
        # TODO избавиться от вложенности
        if self._has_package(relative_path):
            if self.packages:
                for package in self.packages:
                    if relative_path.startswith(package.replace('.', '/')):
                        return True
                    else:
                        continue

                else:
                    return False
            return True

        elif 'root' in self.packages or not self.packages:
            return True

        return False


    @staticmethod
    def _has_package(relative_path: str) -> bool:
        """Проверяем, содержит ли путь хотя бы один пакет (например, есть ли в пути '/')"""
        return '/' in relative_path


    def _check_exists_path(self, raw_packages):

        for package_name in raw_packages:
            abs_path = Path(self.base_path) / package_name.replace(".", "/")
            if package_name == 'root':
                continue
            if not abs_path.exists():
                raise PackageNotFound(package_name=package_name)

    @classmethod
    def _remove_substrings(cls, set_: set[str]) -> set[str]:
        """Удалить из множества строк те элементы, которые являются 'подстроками' других элементов."""
        result = set(set_)  # Создаем копию множества для безопасного удаления

        for x in set_:
            for j in set_:
                if x != j and j.startswith(x) and (len(j) > len(x) and j[len(x)] == '.'):
                    result.discard(j)  # Удаляем элемент j, если он является подстрокой x

        return result


class FilterModules(logging.Filter):
    def filter(self, record: CustomLogRecord) -> bool:
        # absolute_path = Path(record.pathname)
        # relative_path = absolute_path.relative_to(BASE_PATH)
        return True
        # if record.msg != 'error':
        #     return True
        # else:
        #     return False
