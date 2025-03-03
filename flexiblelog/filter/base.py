from pathlib import Path
from typing import Type


class BaseList:
    def __init__(self, base_path: Path, raw_items: str):
        self.base_path = base_path
        self._items_dot = self._clear_empty_item(set(raw_items.split(', ')))
        self._items_paths = self._to_path(self._items_dot)


    def _validate(self, exception_class: Type[Exception]):
        for item_path_name in self._items_paths:
            abs_path = Path(self.base_path / item_path_name)
            if item_path_name == 'root':
                continue
            if not abs_path.exists():
                raise exception_class(item_path_name)

    @staticmethod
    def _clear_empty_item(arr: set[str]) -> set[str]:
        """Удаляет пустые элементы из списка."""
        return {item.strip() for item in arr if item != ''}

    @staticmethod
    def _to_path(seq: set[str]) -> set[str]:
        """Преобразует элементы в пути."""
        raise NotImplementedError("Метод _to_path должен быть реализован в дочернем классе.")

    def __str__(self) -> str:
        return ', '.join(sorted(self._items_dot))


