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

    async def worker(self, task):
        logger.debug("Выполнена таска: ", task, sep=": ")

