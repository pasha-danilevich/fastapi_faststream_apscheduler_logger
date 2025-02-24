import os


class ProjectFolders:
    def __init__(self, base_path, gitignore_path=None):
        self.base_path = base_path
        self.gitignore_path = gitignore_path
        self.ignore_patterns = set()
        self.folders = set()

        if self.gitignore_path and os.path.exists(self.gitignore_path):
            self._load_gitignore()

    def _load_gitignore(self):
        """Загружает шаблоны из .gitignore и преобразует их в набор игнорируемых папок."""
        with open(self.gitignore_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):  # Игнорируем пустые строки и комментарии
                    if line.endswith("/"):  # Если строка заканчивается на "/", это папка
                        self.ignore_patterns.add(line.rstrip("/"))
                    elif os.path.isdir(os.path.join(self.base_path, line)):  # Проверяем, является ли это папкой
                        self.ignore_patterns.add(line)

    def _is_ignored(self, folder_name):
        """Проверяет, нужно ли игнорировать папку."""
        return folder_name in self.ignore_patterns

    def get_folders(self):
        """Возвращает список всех папок проекта, исключая игнорируемые."""
        self._scan_folders(self.base_path)
        return self.folders

    def _scan_folders(self, current_path, prefix=""):
        """Рекурсивно обходит директории и собирает папки."""
        for item in os.listdir(current_path):
            item_path = os.path.join(current_path, item)
            if os.path.isdir(item_path):
                folder_name = f"{prefix}.{item}" if prefix else item
                if not self._is_ignored(item):  # Игнорируем папки из .gitignore
                    self.folders.add(folder_name)
                    self._scan_folders(item_path, folder_name)
