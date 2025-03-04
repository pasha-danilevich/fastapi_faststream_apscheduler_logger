import pytest

from base_test import BaseTest
from flexiblelog.exceptions import NotExist
from flexiblelog.filter.packages import PackageList





class TestPackageListInitialization(BaseTest):
    """Тестирование инициализации и валидации PackageList."""

    def test_package_list_initialization_and_validation(self, temp_project):
        """Тестирует инициализацию и валидацию PackageList."""
        # Корректные пакеты
        package_list = PackageList(temp_project, "api, api.routers, bg.routers", )
        assert package_list.packages_dot == {'api', 'bg.routers'}
        assert package_list.packages == {'api', 'bg/routers'}

        # Некорректный пакет
        with pytest.raises(NotExist):
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
        package_list = PackageList(temp_project, "api, api.routers, bg.routers")
        assert str(package_list) == "api, bg.routers"

        package_list = PackageList(temp_project, "")
        assert str(package_list) == ""

    # Тестирование с пакетом 'root'
    def test_root_package(self, temp_project):
        package_list = PackageList(temp_project, "root")
        assert package_list.packages_dot == {"root"}
        assert package_list.packages == {"root"}


    # Тестирование с вложенными пакетами
    def test_nested_packages(self, temp_project):
        package_list = PackageList(temp_project, "bg.routers, bg.services")
        assert package_list.packages_dot == {"bg.routers", "bg.services"}
        assert package_list.packages == {"bg/routers", "bg/services"}

        package_list = PackageList(temp_project, "bg.routers, bg.services, bg")
        assert package_list.packages_dot == {"bg"}
        assert package_list.packages == {"bg"}

    # Тестирование с дублирующимися пакетами
    def test_duplicate_packages(self, temp_project):
        package_list = PackageList(temp_project, "api, api, bg")
        assert package_list.packages_dot == {"api", "bg"}
        assert package_list.packages == {"api", "bg"}
