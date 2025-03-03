import pytest

from base_test import BaseTest
from flexiblelog.exceptions import ModulNotFound
from flexiblelog.filter.moduls import ModulsList


class TestModulsListInitialization(BaseTest):
    """Тесты для инициализации и валидации класса ModulsList."""

    def test_valid_moduls(self, temp_project):
        """Тест инициализации с корректными модулями."""

        raw_modules = "api.api.py, api.routers.some.py, bg.config.py, main_api.py"
        moduls_list = ModulsList(temp_project, raw_modules)

        # Проверяем, что модули корректно инициализированы
        assert moduls_list.moduls_dot == {"main_api.py", "api.api.py", "api.routers.some.py", "bg.config.py"}
        assert moduls_list.moduls == {"main_api.py", "api/api.py", "bg/config.py", "api/routers/some.py"}

        # Проверяем, что валидация формата проходит без ошибок
        moduls_list._validate_format()

    def test_invalid_moduls_format(self, temp_project):
        """Тест инициализации с некорректным форматом модулей."""
        raw_modules = "api.api.py, api.routers.some"
        moduls_list = ModulsList(temp_project, raw_modules)

        # # Проверяем, что модули корректно инициализированы
        # assert moduls_list.moduls_dot == {"api.api", "api.routers.some"}
        # assert moduls_list.moduls == {"api/api.py", "api/routers/some.py"}

        # Проверяем, что валидация формата выбрасывает исключение
        with pytest.raises(ValueError) as exc_info:
            moduls_list._validate_format()
        assert 'Не верный формат модуля: api.routers.some. Все модули должны заканчиваться на ".py"' == str(
            exc_info.value)

    def test_empty_moduls(self, temp_project):
        """Тест инициализации с пустым списком модулей."""
        raw_modules = ""
        moduls_list = ModulsList(temp_project, raw_modules)

        # Проверяем, что модули корректно инициализированы (пустой список)
        assert moduls_list.moduls_dot == set()
        assert moduls_list.moduls == set()

        # Проверяем, что валидация формата проходит без ошибок
        moduls_list._validate_format()

    def test_moduls_with_whitespace(self, temp_project):
        """Тест инициализации с модулями, содержащими пробелы."""
        raw_modules = "  api.api.py  ,  api.routers.some.py  "
        moduls_list = ModulsList(temp_project, raw_modules)

        # Проверяем, что модули корректно инициализированы (пробелы удалены)
        assert moduls_list.moduls_dot == {"api.api.py", "api.routers.some.py"}
        assert moduls_list.moduls == {"api/api.py", "api/routers/some.py"}

        # Проверяем, что валидация формата проходит без ошибок
        moduls_list._validate_format()
