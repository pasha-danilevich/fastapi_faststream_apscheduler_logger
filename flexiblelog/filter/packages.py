from pathlib import Path

from flexiblelog.exceptions import NotExist
from flexiblelog.filter.base import BaseList


class PackageList(BaseList):
    def __init__(self, base_path: Path, raw_packages: str):
        self.packages_dot = self._remove_substrings(self._clear_empty_item(set(raw_packages.split(', '))))
        self.packages = self._to_path(self.packages_dot)

        self._validate_existing(base_path, self.packages)

    @staticmethod
    def _validate_existing(base_path, seq):
        for item_path_name in seq:
            if item_path_name == 'root':
                continue
            abs_path = Path(base_path / item_path_name)

            if not abs_path.exists():
                raise NotExist(item_path_name)



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
        return self.view_items(self.packages_dot)






