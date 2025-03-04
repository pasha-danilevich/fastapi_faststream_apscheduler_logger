import logging
from pathlib import Path
from unittest.mock import patch
import pytest

from base_test import BaseTest
from flexiblelog.filter.filter import FilterModules
from flexiblelog.filter.moduls import ModulsList
from flexiblelog.schemas import FilterType


# Замените `your_module` на имя вашего модуля



class TestFilterModules(BaseTest):
    """Тесты для фильтрации модулей."""

    def test_filter_modules_only_mode(self, temp_project):
        """
        Тестирует фильтр в режиме ONLY (логируются только указанные модули).
        """
        # TODO: проверять точнее:
        # "api.routers.some.py".endswith('some.py')
        # True
        # "api.routers.some.py".endswith('ome.py')
        # True
        # Настраиваем логгер
        logger = logging.getLogger("test_filter_modules_only_mode")
        logger.setLevel(logging.DEBUG)

        # Создаем фильтр
        modules = "api.api.py, bg.app.py"
        modules_obj = ModulsList(temp_project, modules)
        filter_modules = FilterModules(modules_obj.moduls, FilterType.ONLY, temp_project)
        logger.addFilter(filter_modules)

        # Имитируем логи из разных модулей
        with patch("logging.LogRecord") as mock_record:
            # Лог из api/api.py
            mock_record.pathname = str(temp_project / "api" / "api.py")
            assert logger.filter(mock_record) is True, "Лог из api/api.py должен быть пропущен"

            # Лог из bg/app.py
            mock_record.pathname = str(temp_project / "bg" / "app.py")
            assert logger.filter(mock_record) is True, "Лог из bg/app.py должен быть пропущен"

            # Лог из main_api.py
            mock_record.pathname = str(temp_project / "main_api.py")
            assert logger.filter(mock_record) is False, "Лог из main_api.py должен быть заблокирован"

    def test_filter_modules_only_mode_2(self, temp_project):
        """
        Тестирует фильтр в режиме ONLY (логируются только указанные модули).
        """
        # Настраиваем логгер
        logger = logging.getLogger("test_filter_modules_only_mode_2")
        logger.setLevel(logging.DEBUG)

        # Создаем фильтр
        modules = "api.py"

        modules_obj = ModulsList(temp_project, modules)
        filter_modules = FilterModules(modules_obj.moduls, FilterType.ONLY, temp_project)
        logger.addFilter(filter_modules)

        # Имитируем логи из разных модулей
        with patch("logging.LogRecord") as mock_record:
            # Лог из api/api.py
            mock_record.pathname = str(temp_project / "api" / "api.py")
            assert logger.filter(mock_record) is True, "Лог из api/api.py должен быть пропущен"

            # Лог из bg/app.py
            mock_record.pathname = str(temp_project / "bg" / "api.py")
            assert logger.filter(mock_record) is True, "Лог из bg/app.py должен быть пропущен"

            # Лог из main_api.py
            mock_record.pathname = str(temp_project / "utils.py")
            assert logger.filter(mock_record) is False, "Лог из utils.py должен быть заблокирован"

            mock_record.pathname = str(temp_project / "main_api.py")
            assert logger.filter(mock_record) is False, "Лог из main_api.py должен быть заблокирован"

    def test_filter_modules_only_mode_3(self, temp_project):
        """
        Тестирует фильтр в режиме ONLY (логируются только указанные модули).
        """
        # Настраиваем логгер
        logger = logging.getLogger("test_filter_modules_only_mode_3")
        logger.setLevel(logging.DEBUG)

        # Создаем фильтр
        modules = "settings.py"

        modules_obj = ModulsList(temp_project, modules)
        filter_modules = FilterModules(modules_obj.moduls, FilterType.ONLY, temp_project)
        logger.addFilter(filter_modules)

        # Имитируем логи из разных модулей
        with patch("logging.LogRecord") as mock_record:
            # Лог из api/api.py
            mock_record.pathname = str(temp_project / "api" / "api.py")
            assert logger.filter(mock_record) is False, "Лог из api/api.py должен быть заблокирован"

            # Лог из bg/app.py
            mock_record.pathname = str(temp_project / "bg" / "api.py")
            assert logger.filter(mock_record) is False, "Лог из bg/app.py должен быть заблокирован"

            # Лог из main_api.py
            mock_record.pathname = str(temp_project / "utils.py")
            assert logger.filter(mock_record) is False, "Лог из utils.py должен быть заблокирован"

    def test_filter_modules_without_mode(self, temp_project):
        """
        Тестирует фильтр в режиме WITHOUT (логируются все, кроме указанных модулей).
        """
        # Настраиваем логгер
        logger = logging.getLogger("test_filter_modules_without_mode")
        logger.setLevel(logging.DEBUG)

        # Создаем фильтр

        modules = "api.api.py, bg.app.py"
        modules_obj = ModulsList(temp_project, modules)
        filter_modules = FilterModules(modules_obj.moduls, FilterType.WITHOUT, temp_project)
        logger.addFilter(filter_modules)

        # Имитируем логи из разных модулей
        with patch("logging.LogRecord") as mock_record:
            # Лог из api/api.py
            mock_record.pathname = str(temp_project / "api" / "api.py")
            assert logger.filter(mock_record) is False, "Лог из api/api.py должен быть заблокирован"

            # Лог из bg/app.py
            mock_record.pathname = str(temp_project / "bg" / "app.py")
            assert logger.filter(mock_record) is False, "Лог из bg/app.py должен быть пропущен"

            # Лог из main_api.py
            mock_record.pathname = str(temp_project / "main_api.py")
            assert logger.filter(mock_record) is True, "Лог из main_api.py должен быть пропущен"

