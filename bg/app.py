import asyncio
from faststream import FastStream
from bg.config import broker
from logger_config import logger
from .routers.bg_router import router as router_task


# Инициализация брокера и FastStream
app = FastStream(broker)


async def bg_app():
    broker.include_router(router_task)

    await app.run()
