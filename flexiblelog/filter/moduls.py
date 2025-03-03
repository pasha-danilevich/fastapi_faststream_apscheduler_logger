from pathlib import Path

from flexiblelog.exceptions import ModulNotFound
from flexiblelog.filter.base import BaseList


class ModulsList(BaseList):
    def __init__(self, base_path: Path, raw_modules: str):
        super().__init__(base_path, raw_modules)
        self.moduls_dot = self._items_dot
        self.moduls = self._items_paths


    def _validate(self, exception_class=ModulNotFound):
        super()._validate(exception_class)

    def _validate_format(self):
        for modul in self.moduls_dot:
            if '.py' not in modul:
                raise ValueError(f'Не верный формат модуля: {modul}. Все модули должны заканчиваться на ".py"')

    @staticmethod
    def _to_path(seq: set[str]) -> set[str]:
        """Преобразует имена модулей в пути."""
        path_like = {text[:-3].replace('.', '/') for text in seq}
        return {f'{text}.py' for text in path_like}



