from pathlib import Path

from flexiblelog.exceptions import PackageNotFound


class PackageList:
    def __init__(self, base_path: Path, raw_packages: str):
        self.base_path = base_path
        self.packages_dot = self._remove_substrings(self._clear_empty_item(set(raw_packages.split(', '))))
        self.packages = self._to_path(self.packages_dot)

        self._validate()

    def _validate(self):
        for package_name in self.packages:
            abs_path = Path(self.base_path) / package_name.replace(".", "/")
            if package_name == 'root':
                continue
            if not abs_path.exists():
                raise PackageNotFound(package_name=package_name)

    @staticmethod
    def _clear_empty_item(arr: set[str]) -> set[str]:
        """Удаляет пустые элементы из списка.

        Примеры:
        - [''] -> []
        - ['name', ''] -> ['name']
        """
        return {item.strip() for item in arr if item != ''}

    @staticmethod
    def _to_path(packages: set[str]) -> set[str]:
        return {package.replace('.', '/') for package in packages}

    @classmethod
    def _remove_substrings(cls, set_: set[str]) -> set[str]:
        """Удалить из множества строк те элементы, которые являются 'подстроками' других элементов."""
        result = set(set_)  # Создаем копию множества для безопасного удаления

        for x in set_:
            for j in set_:
                if x != j and j.startswith(x) and (len(j) > len(x) and j[len(x)] == '.'):
                    result.discard(j)  # Удаляем элемент j, если он является подстрокой x

        return result

    def __str__(self) -> str:
        return ', '.join(self.packages_dot)


if __name__ == "__main__":
    B = Path('/home/pavel/PycharmProjects/fastapi_faststream_apscheduler_logger')
    r = 'api, bg.routers'

    l = PackageList(B, raw_packages=r)
    print(l)
    print(l.packages)
