from pathlib import Path

from flexiblelog.exceptions import PackageNotFound
from flexiblelog.filter.base import BaseList


class PackageList(BaseList):
    def __init__(self, base_path: Path, raw_packages: str):
        super().__init__(base_path, raw_packages)

        self.packages_dot = self._remove_substrings(self._items_dot)
        self.packages = self._to_path(self.packages_dot)
        self._validate()

    def _validate(self, exception_class=PackageNotFound):
        super()._validate(exception_class)

    @staticmethod
    def _to_path(packages: set[str]) -> set[str]:
        """Преобразует имена пакетов в пути."""
        return {package.replace('.', '/') for package in packages}

    @classmethod
    def _remove_substrings(cls, set_: set[str]) -> set[str]:
        """Удаляет из множества строк те элементы, которые являются 'подстроками' других элементов."""
        result = set(set_)  # Создаем копию множества для безопасного удаления

        for x in set_:
            for j in set_:
                if x != j and j.startswith(x) and (len(j) > len(x) and j[len(x)] == '.'):
                    result.discard(j)  # Удаляем элемент j, если он является подстрокой x

        return result

    def __str__(self) -> str:
        return ', '.join(sorted(self.packages_dot))






