import pytest
from pathlib import Path
import tempfile


class BaseTest:
    """Базовый класс для тестов, содержащий общие фикстуры и методы."""

    @pytest.fixture(scope="session")
    def temp_project(self):
        """Создает временную структуру директорий и файлов."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base_path = Path(tmpdir)

            # Создаем структуру проекта
            # Директория api
            (base_path / "api").mkdir()
            (base_path / "api" / "api.py").touch()
            (base_path / "api" / "routers").mkdir()
            (base_path / "api" / "routers" / "routers").mkdir()
            (base_path / "api" / "routers" / "routers" / "some.py").touch()
            (base_path / "api" / "routers" / "some.py").touch()

            # Директория bg
            (base_path / "bg").mkdir()
            (base_path / "bg" / "app.py").touch()
            (base_path / "bg" / "config.py").touch()
            (base_path / "bg" / "routers").mkdir()
            (base_path / "bg" / "routers" / "bg_router.py").touch()
            (base_path / "bg" / "services").mkdir()
            (base_path / "bg" / "services" / "__init__.py").touch()
            (base_path / "bg" / "services" / "schedulers.py").touch()
            (base_path / "bg" / "services" / "workers.py").touch()

            # Корневые файлы
            (base_path / "logger").mkdir()
            (base_path / "logger.py").touch()
            (base_path / "main_api.py").touch()
            (base_path / "main_bg.py").touch()
            (base_path / "requirements.txt").touch()
            (base_path / "sandbox.py").touch()
            (base_path / "schemas.py").touch()
            (base_path / "settings.py").touch()

            yield base_path