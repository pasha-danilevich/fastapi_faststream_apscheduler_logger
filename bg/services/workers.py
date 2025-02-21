from logger_config import logger
from schemas import BgTask, BgTasks


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
