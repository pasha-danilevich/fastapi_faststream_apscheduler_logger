import logging
import tempfile
from pathlib import Path

from unittest.mock import patch

from base_test import BaseTest
from flexiblelog.schemas import FilterType
from flexiblelog.filter.filter import FilterPackages


class TestFilterPackages(BaseTest):



    def test_filter_packages_only_mode(self, temp_project):
        """
        Тестирует фильтр в режиме ONLY (логируются только указанные пакеты).
        """
        # Настраиваем логгер
        logger = logging.getLogger("test_filter_packages_only_mode")
        logger.setLevel(logging.DEBUG)

        # Создаем фильтр
        packages = ["api", "bg"]
        filter_packages = FilterPackages(packages, FilterType.ONLY, temp_project)
        logger.addFilter(filter_packages)
        print(temp_project)

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

    def test_filter_packages_without_mode(self, temp_project):
        """
        Тестирует фильтр в режиме WITHOUT (логируются все, кроме указанных пакетов).
        """
        # Настраиваем логгер
        logger = logging.getLogger("test_filter_packages_without_mode")
        logger.setLevel(logging.DEBUG)

        # Создаем фильтр
        packages = ["api"]
        filter_packages = FilterPackages(packages, FilterType.WITHOUT, temp_project)
        logger.addFilter(filter_packages)

        print(temp_project)
        # Имитируем логи из разных модулей
        with patch("logging.LogRecord") as mock_record:
            # Лог из api/api.py
            mock_record.pathname = str(temp_project / "api" / "api.py")
            print(mock_record.pathname)
            assert logger.filter(mock_record) is False, "Лог из api/api.py должен быть заблокирован"

            # Лог из bg/app.py
            mock_record.pathname = str(temp_project / "bg" / "app.py")
            assert logger.filter(mock_record) is True, "Лог из bg/app.py должен быть пропущен"

            # Лог из main_api.py
            mock_record.pathname = str(temp_project / "main_api.py")
            assert logger.filter(mock_record) is True, "Лог из main_api.py должен быть пропущен"


    def test_filter_packages_root(self, temp_project):
        """
        Тестирует фильтр с включенным пакетом 'root'.
        """
        # Настраиваем логгер
        logger = logging.getLogger("test_filter_packages_root")
        logger.setLevel(logging.DEBUG)

        # Создаем фильтр
        packages = ["root"]
        filter_packages = FilterPackages(packages, FilterType.ONLY, temp_project)
        logger.addFilter(filter_packages)

        # Имитируем логи из разных модулей
        with patch("logging.LogRecord") as mock_record:
            # Лог из main_api.py
            mock_record.pathname = str(temp_project / "main_api.py")
            assert logger.filter(mock_record) is True, "Лог из main_api.py должен быть пропущен"

            # Лог из api/api.py
            mock_record.pathname = str(temp_project / "api" / "api.py")
            assert logger.filter(mock_record) is False, "Лог из api/api.py должен быть заблокирован"