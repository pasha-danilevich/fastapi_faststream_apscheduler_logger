import pytest

from base_test import BaseTest
from flexiblelog.exceptions import NotExist
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



    def test_invalid_moduls_format(self, temp_project):
        """Тест инициализации с некорректным форматом модулей."""
        raw_modules = "api.api.py, api.routers.some"



        # Проверяем, что валидация формата выбрасывает исключение
        with pytest.raises(ValueError) as exc_info:
            ModulsList(temp_project, raw_modules)

        assert 'Не верный формат модуля: api.routers.some. Все модули должны заканчиваться на ".py"' == str(exc_info.value)

    def test_invalid_moduls_format_2(self, temp_project):
        """Тест инициализации с некорректным форматом модулей."""
        raw_modules = "api.api.py, api.routers"

        # Проверяем, что валидация формата выбрасывает исключение ValueError
        with pytest.raises(ValueError) as exc_info:
            ModulsList(temp_project, raw_modules)

        # Проверяем сообщение исключения
        assert 'Не верный формат модуля: api.routers. Все модули должны заканчиваться на ".py"' in str(exc_info.value)

    def test_nonexistent_module(self, temp_project):
        """Тест инициализации с несуществующим модулем."""
        raw_modules = "api.api.py, nonexistent_module.py"

        # Проверяем, что валидация существования модуля выбрасывает исключение NotExist
        with pytest.raises(NotExist) as exc_info:
            ModulsList(temp_project, raw_modules)

        # Проверяем сообщение исключения

        assert "nonexistent_module.py" in str(exc_info.value)



    def test_empty_moduls(self, temp_project):
        """Тест инициализации с пустым списком модулей."""
        raw_modules = ""
        moduls_list = ModulsList(temp_project, raw_modules)

        # Проверяем, что модули корректно инициализированы (пустой список)
        assert moduls_list.moduls_dot == set()
        assert moduls_list.moduls == set()


    def test_moduls_with_whitespace(self, temp_project):
        """Тест инициализации с модулями, содержащими пробелы."""
        raw_modules = "  api.api.py  ,  api.routers.some.py  "
        moduls_list = ModulsList(temp_project, raw_modules)

        # Проверяем, что модули корректно инициализированы (пробелы удалены)
        assert moduls_list.moduls_dot == {"api.api.py", "api.routers.some.py"}
        assert moduls_list.moduls == {"api/api.py", "api/routers/some.py"}



    def test_moduls_wrong_module(self, temp_project):
        raw_modules = "p.py"

        with pytest.raises(NotExist) as exc_info:
            ModulsList(temp_project, raw_modules)

        assert 'Not exist: p.py' == str(exc_info.value)

    def test_moduls_wrong_module_2(self, temp_project):
        raw_modules = "root"

        with pytest.raises(ValueError) as exc_info:
            ModulsList(temp_project, raw_modules)

        assert 'Не верный формат модуля: root. Все модули должны заканчиваться на ".py"' == str(exc_info.value)
