import logging
import os

from logger.folders import ProjectFolders
from logger.utils import clear_empty_item, subtract_sets
from settings import BASE_PATH, FilterType
from settings import settings as stt

gitignore_path = os.path.join(BASE_PATH, ".gitignore")  # Путь к .gitignore
project_folders = ProjectFolders(BASE_PATH, gitignore_path)
all_folders: set = project_folders.get_folders()
all_folders.add('root')

PACKAGES_LIST = set(clear_empty_item(stt.LOG_PACKAGES.split(', ')))
PACKAGES_FILTERS_TYPE = stt.LOG_PACKAGES_FILTER_TYPE

if PACKAGES_FILTERS_TYPE == FilterType.WITHOUT.value:
    PACKAGES_LIST =  subtract_sets(all_folders, PACKAGES_LIST)

MODULES_FILTER_TYPE = stt.LOG_MODULES_FILTER_TYPE
MODULES_LIST = set(clear_empty_item(stt.LOG_MODULES.split(', ')))



from logger.filter import FuncArgsFilter, FilterPackages, FilterModules
from logger.formatter import Formatter
from logger.record import custom_log_record_factory

console_handler = logging.StreamHandler()

logging.setLogRecordFactory(custom_log_record_factory)

console_handler.addFilter(FuncArgsFilter())

filter_packages = FilterPackages(PACKAGES_LIST, PACKAGES_FILTERS_TYPE)
console_handler.addFilter(filter_packages)

console_handler.addFilter(FilterModules())

# Создаем форматтер и добавляем его в обработчик
console_handler.setFormatter(Formatter())

logger = logging.getLogger(stt.LOGGER_NAME)
logger.setLevel(stt.LOG_LEVEL)
logger.addHandler(console_handler)

logger.info(
    (f'logging {PACKAGES_FILTERS_TYPE.value}: {stt.LOG_PACKAGES.split(", ")} packages'
    if PACKAGES_LIST else 'Logging ALL packages')
    + ' and ' +
    (f'{MODULES_FILTER_TYPE.value}: {stt.LOG_MODULES.split(", ")} modules'
    if MODULES_LIST else 'ALL modules')
)
