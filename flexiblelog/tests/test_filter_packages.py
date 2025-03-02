import pytest

from base_test import BaseTest
from flexiblelog.filter.packages import PackageList
from flexiblelog.exceptions import PackageNotFound




class TestPackageListInitialization(BaseTest):
    """Тестирование инициализации и валидации PackageList."""

    def test_package_list_initialization_and_validation(self, temp_project):
        """Тестирует инициализацию и валидацию PackageList."""
        # Корректные пакеты
        package_list = PackageList(temp_project, "api, models, api.api, test, models.a.b.c, services.main", )
        assert package_list.packages_dot == {'models', 'test', 'api', 'services.main'}
        assert package_list.packages == {'models', 'test', 'api', 'services/main'}

        # Некорректный пакет
        with pytest.raises(PackageNotFound):
            PackageList(temp_project, "invalid_package")

    # Тестирование метода _clear_empty_item
    def test_clear_empty_item(self):
        assert PackageList._clear_empty_item({"", "api", "models"}) == {"api", "models"}
        assert PackageList._clear_empty_item({"", ""}) == set()
        assert PackageList._clear_empty_item({"api"}) == {"api"}

    # Тестирование метода _to_path
    def test_to_path(self):
        assert PackageList._to_path({"api.v1", "models"}) == {"api/v1", "models"}
        assert PackageList._to_path({"api"}) == {"api"}
        assert PackageList._to_path(set()) == set()

    # Тестирование метода _remove_substrings
    def test_remove_substrings(self):
        assert PackageList._remove_substrings({"api", "api.v1"}) == {"api"}
        assert PackageList._remove_substrings({"api.v1", "api.v2"}) == {"api.v1", "api.v2"}
        assert PackageList._remove_substrings({"api", "models"}) == {"api", "models"}
        assert PackageList._remove_substrings({"api.v1.models", "api.v1"}) == {"api.v1"}

    # Тестирование строкового представления
    def test_str_representation(self, temp_project):
        package_list = PackageList(temp_project, "api, models, services.main")
        assert str(package_list) == "api, models, services.main"

        package_list = PackageList(temp_project, "")
        assert str(package_list) == ""

    # Тестирование с пакетом 'root'
    def test_root_package(self, temp_project):
        package_list = PackageList(temp_project, "root")
        assert package_list.packages_dot == {"root"}
        assert package_list.packages == {"root"}

        # Проверка, что валидация не выбрасывает исключение для 'root'
        package_list._validate()

    # Тестирование с вложенными пакетами
    def test_nested_packages(self, temp_project):
        package_list = PackageList(temp_project, "api.v1, api.v2")
        assert package_list.packages_dot == {"api.v1", "api.v2"}
        assert package_list.packages == {"api/v1", "api/v2"}

        package_list = PackageList(temp_project, "api.v1, api.v2, api")
        assert package_list.packages_dot == {"api"}
        assert package_list.packages == {"api"}

    # Тестирование с дублирующимися пакетами
    def test_duplicate_packages(self, temp_project):
        package_list = PackageList(temp_project, "api, api, models")
        assert package_list.packages_dot == {"api", "models"}
        assert package_list.packages == {"api", "models"}
