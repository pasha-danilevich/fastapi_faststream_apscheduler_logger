# flexiblelog

### Данный пакет предоставляет гибкую, настраиваемую, систему логгирования и легкую интеграции в проект 
 

```python
   # Import `LoggerSettings` and `create_logger`:
   from logger import create_logger
   from logger.schemas import LoggerSettings
  ```


```python
# Create a LoggerSettings object with your desired configuration:
logger_settings = LoggerSettings(
    LOGGER_NAME="my-logger",
    LEVEL="DEBUG",
    MODE="DEV",
    PACKAGES_FILTER_TYPE="ONLY",
    PACKAGES="package1, package2",
    MODULES_FILTER_TYPE="WITHOUT",
    MODULES="module1, module2"
)
```


```python
# Create the logger:
BASE_PATH = YOUR_BASE_PATH
logger = create_logger(base_path=BASE_PATH, settings=logger_settings)
```



```python
# Use the logger:
logger.info("Logger is ready!")
```

## Settings

#### LOGGER_NAME
Установите имя логгера

---

#### LEVEL
Уровни логгирования ведут себя так же как и в стандартной библиотеке logging
https://docs.python.org/3/library/logging.html#logging-levels

---

#### MODE
...

---

#### PACKAGES_FILTER_TYPE & MODULES_FILTER_TYPE
Типы фильтрации пакетов/модулей:
- `ONLY` - логгировать только эти пакеты 
- `WITHOUT` - логгировать все пакеты, за исключение этих

---

#### PACKAGES & MODULES
Список пакетов/модулей python.

1. Список пакетов и модулей перечислить через запятую с пробелом.
```python
PACKAGES/MODULES='name, name, name'
```

2. Включены все, если ничего не передавать. 
```python
PACKAGES/MODULES='' 
# в не зависимости от PACKAGES/MODULES_RULE
```

3. Если необходимо включить/исключить вложенный пакет,
необходимо прописать через точку родительские пакеты.

```python
PACKAGES='name, name.in_some, name.in_some.some_some'
```


4. Logger сперва включает пакеты/модули затем исключает
```python
PACKAGES_RULE='ONLY'
PACKAGES='api, models, test'

MODULES_RULE='WITHOUT'
MODULES='test_file.py'

# Итог: логгированию подлежат пакеты: api, models и все модули в пакете test кроме test_file.py
```


5. Более высокая иерархия пакетов перекроет низшую во время включения.
```python
PACKAGES_RULE='ONLY'
PACKAGES='api.v2, bg, service, api, api.service, bg.routers, api.service.v1'

# Итог: логгированию подлежат пакеты (bg, service, api)
```



6. Если хотите включить/исключить все модули, находящиеся в корне проекта
(модули, не находящиеся в каком-либо пакете), добавьте "root"
в PACKAGES
```python
PACKAGES='root'
```

## Ваши форматеры 
Вы можете передать ваш класс унаследованный от `logging.Formatter`
```python
import logging

from flexiblelog import LoggerSettings, create_logger
from settings import settings, BASE_PATH

logger_settings = LoggerSettings(
    LOGGER_NAME=settings.LOGGER_NAME,
    LEVEL=settings.LOG_LEVEL,
    MODE=settings.LOG_MODE,
    PACKAGES_FILTER_TYPE=settings.LOG_PACKAGES_FILTER_TYPE,
    PACKAGES=settings.LOG_PACKAGES,
    MODULES_FILTER_TYPE=settings.LOG_MODULES_FILTER_TYPE,
    MODULES=settings.LOG_MODULES,
)


class MyFormatter(logging.Formatter):
    """Your Formatter class"""
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    def __init__(self, fmt=fmt, datefmt=None):
        logging.Formatter.__init__(self, fmt, datefmt)


logger = create_logger(
    base_path=BASE_PATH, 
    settings=logger_settings, 
    formatter_class=MyFormatter, # передайте свой форматер 
)
```