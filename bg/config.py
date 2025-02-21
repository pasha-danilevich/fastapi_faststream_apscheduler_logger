import functools

from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from faststream.rabbit import RabbitBroker

from settings import settings
from logger_config import logger


scheduler = AsyncIOScheduler(
    jobstores={
        "default": RedisJobStore(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            db=settings.REDIS_STORE_DB_INDEX,
        )
    }
)

BROKER_CONN_URI = f"amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASS}@{settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}/"
broker = RabbitBroker(url=BROKER_CONN_URI)


def broker_session(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        async with broker as br:
            logger.debug(f"Функция {func.__name__} стала сессией брокера ")
            return await func(br, *args, **kwargs)

    return wrapper
