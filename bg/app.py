import asyncio
from faststream import FastStream
from bg.config import broker
from logger import logger
from .routers.bg_router import router as router_task


# Инициализация брокера и FastStream
app = FastStream(broker)
def some_bg():
    logger.info('Starting some task')

async def bg_app():
    logger.info("Starting background task")
    broker.include_router(router_task)
    await app.run()
