import os
from pathlib import Path

from flexiblelog.exceptions import NotExist
from flexiblelog.filter.base import BaseList


class ModulsList(BaseList):
    def __init__(self, base_path: Path, raw_modules: str):
        self.moduls_dot = self._clear_empty_item(set(raw_modules.split(', ')))
        self.moduls = self._to_path(self.moduls_dot)

        self._validate_format(self.moduls_dot)
        self._validate_existing(base_path, self.moduls)

    @staticmethod
    def _validate_existing(base_path: Path, seq):
        for file_name in seq:
            result = []
            file_name = file_name.split('/')[-1]
            for root, dirs, filenames in os.walk(base_path):
                # Исключаем папку .venv из дальнейшего обхода
                if '.venv' in dirs:
                    dirs.remove('.venv')

                # Ищем файл с указанным именем
                for f in filenames:
                    if file_name is None or os.path.basename(f).split('/')[-1] == file_name:
                        result.append(os.path.join(root, f))

            if not result:
                raise NotExist(item_name=file_name)

    @staticmethod
    def _validate_format(moduls: set[str]):
        for modul in moduls:
            if not modul.endswith('.py'):
                raise ValueError(f'Не верный формат модуля: {modul}. Все модули должны заканчиваться на ".py"')

    @staticmethod
    def _to_path(seq: set[str]) -> set[str]:
        """Преобразует имена модулей в пути."""
        path_like = {text[:-3].replace('.', '/') for text in seq}
        return {f'{text}.py' for text in path_like}

    def __str__(self):
        return super().view_items(self.moduls_dot)
