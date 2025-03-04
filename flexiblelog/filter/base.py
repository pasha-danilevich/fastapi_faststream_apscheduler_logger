class BaseList:

    @staticmethod
    def _clear_empty_item(arr: set[str]) -> set[str]:
        """Удаляет пустые элементы из списка."""
        return {item.strip() for item in arr if item != ''}

    @staticmethod
    def view_items(items: set[str]) -> str:
        return ', '.join(sorted(items))
