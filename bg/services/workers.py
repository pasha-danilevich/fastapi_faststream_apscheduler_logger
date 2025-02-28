from logger import logger
from schemas import BgTasks


def some_sql_func(sql):
    logger.debug('Do some with sql', extra={'full_args_length': True})


class BgWorker:

    def __init__(self):
        pass

    @staticmethod
    async def pinger(tasks: BgTasks):
        logger.debug(f"Проведены необходимые проверки доступности {tasks}")
        return tasks

    @staticmethod
    async def sender(tasks: BgTasks):
        logger.debug("Получены таски")
        return tasks

    @staticmethod
    async def worker(task):
        logger.debug(f"Выполнена таска: {task}")
