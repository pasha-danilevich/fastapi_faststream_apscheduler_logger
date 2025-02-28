# flexiblelog

### Данный пакет предоставляет гибкую, настраиваемую, систему логгирования и легкую интеграции в проект 
 
## Get started
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

## Форматер

Все сообщения выводятся в следующим формате:
```
{path}:{line_nubmer} in {module} > {function}({args}) - {asctime}
{record.levelname} {record.msg}
```
Пример:
```commandline
/home/your_path/api/routers/some.py:4 in some.py > some_some(x: 10, y:12) - 2025-02-28 11:49:16,928
DEBUG:    some_some
```

Иногда значение аргументов бывает слишком большим, для того, чтобы отображать его в консоль, поэтому они урезанны.
Чтобы этого избежать урезания, необходимо в месте вызова логгера, передать `extra={'full_args_length': True}`

Пример кода:
```python
from your_modul import logger # достаем объект логгер из модуля, где он был у вас объявлен

def some_sql_func(sql):
    logger.debug('Do some with sql', extra={'full_args_length': True})
```
Результат:
```commandline
/home/pavel/PycharmProjects/fastapi_faststream_apscheduler_logger/bg/services/workers.py:6 in workers.py > some_sql_func(sql: select count(*)
    from person
    where 1 = 1
      and name is not null
      and {condition};) - 2025-02-28 12:54:56,077
DEBUG:    Do some with sql
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