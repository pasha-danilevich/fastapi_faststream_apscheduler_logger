class PackageNotFound(Exception):
    def __init__(self, package_name: str, message: str = "Package not found"):
        self.package_name = package_name  # Сохраняем имя пакета
        self.message = message  # Сообщение об ошибке
        super().__init__(self.message)

    def __str__(self):
        # Возвращаем строковое представление ошибки
        return f"{self.message}: {self.package_name}"