import pytest
from pathlib import Path
import tempfile


from flexiblelog.filter.packages import PackageList
from flexiblelog.exceptions import PackageNotFound


# Фикстура для создания временной директории
@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


def make_temp_dirs(temp_dir):
    (temp_dir / "api").mkdir()
    (temp_dir / "models").mkdir()
    (temp_dir / "test").mkdir()
    (temp_dir / "services" / "main").mkdir(parents=True)
    (temp_dir / "api" / "v1").mkdir(parents=True)
    (temp_dir / "api" / "v2").mkdir(parents=True)

# Тестирование инициализации и валидации
def test_package_list_initialization_and_validation(temp_dir):
    # Создаем структуру директорий
    make_temp_dirs(temp_dir)

    # Корректные пакеты
    package_list = PackageList(temp_dir, "api, models, api.api, test, models.a.b.c, services.main",)
    assert package_list.packages_dot == {'models', 'test', 'api', 'services.main'}
    assert package_list.packages == {'models', 'test', 'api', 'services/main'}

    # Некорректный пакет
    with pytest.raises(PackageNotFound):
        PackageList(temp_dir, "invalid_package")


# Тестирование метода _clear_empty_item
def test_clear_empty_item():
    assert PackageList._clear_empty_item({"", "api", "models"}) == {"api", "models"}
    assert PackageList._clear_empty_item({"", ""}) == set()
    assert PackageList._clear_empty_item({"api"}) == {"api"}


# Тестирование метода _to_path
def test_to_path():
    assert PackageList._to_path({"api.v1", "models"}) == {"api/v1", "models"}
    assert PackageList._to_path({"api"}) == {"api"}
    assert PackageList._to_path(set()) == set()


# Тестирование метода _remove_substrings
def test_remove_substrings():
    assert PackageList._remove_substrings({"api", "api.v1"}) == {"api"}
    assert PackageList._remove_substrings({"api.v1", "api.v2"}) == {"api.v1", "api.v2"}
    assert PackageList._remove_substrings({"api", "models"}) == {"api", "models"}
    assert PackageList._remove_substrings({"api.v1.models", "api.v1"}) == {"api.v1"}


# Тестирование строкового представления
def test_str_representation(temp_dir):
    make_temp_dirs(temp_dir)

    package_list = PackageList(temp_dir, "api, models, services.main")
    assert str(package_list) == "api, models, services.main"

    package_list = PackageList(temp_dir, "")
    assert str(package_list) == ""


# Тестирование с пакетом 'root'
def test_root_package(temp_dir):
    package_list = PackageList(temp_dir, "root")
    assert package_list.packages_dot == {"root"}
    assert package_list.packages == {"root"}

    # Проверка, что валидация не выбрасывает исключение для 'root'
    package_list._validate()


# Тестирование с вложенными пакетами
def test_nested_packages(temp_dir):
    make_temp_dirs(temp_dir)

    package_list = PackageList(temp_dir, "api.v1, api.v2")
    assert package_list.packages_dot == {"api.v1", "api.v2"}
    assert package_list.packages == {"api/v1", "api/v2"}

    package_list = PackageList(temp_dir, "api.v1, api.v2, api")
    assert package_list.packages_dot == {"api"}
    assert package_list.packages == {"api"}

# Тестирование с дублирующимися пакетами
def test_duplicate_packages(temp_dir):
    make_temp_dirs(temp_dir)

    package_list = PackageList(temp_dir, "api, api, models")
    assert package_list.packages_dot == {"api", "models"}
    assert package_list.packages == {"api", "models"}