
class NotExist(Exception):
    def __init__(self, item_name: str, message: str = "Not exist"):
        self.item_name = item_name  # Сохраняем имя пакета
        self.message = message  # Сообщение об ошибке
        super().__init__(self.message)

    def __str__(self):
        # Возвращаем строковое представление ошибки
        return f"{self.message}: {self.item_name}"