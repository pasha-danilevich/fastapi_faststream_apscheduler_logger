from typing import Annotated

from faststream.rabbit import RabbitRouter
from faststream import Depends

from logger import logger
from schemas import BgTask, BgTasks
from bg.services.workers import BgWorker
from bg.config import broker

router = RabbitRouter()

def some_routers():
    logger.warning('start some_routers')


@router.publisher("sender")
@router.subscriber("pinger")
async def ping(service: Annotated[BgTasks, Depends(BgWorker().pinger)]):
    logger.debug(f"pub: sender, sub: pinger, service:{service}")
    return service
# воркер "pinger" слушает этот эндпоинт, а потом отправляет в "sender"


@router.publisher("worker")
@router.subscriber("sender")
async def send(tasks: Annotated[BgTasks, Depends(BgWorker().sender)]):
    for task in tasks.names:
        logger.debug(f"pub: worker, sub: sender, task:{task}")
        await broker.publish(queue="worker", message=task)


# subscriber - значит слушает, смотрит
@router.subscriber("worker")
async def send(task: str):
    logger.debug(f"sub: worker, task:{task}")
    return await BgWorker().worker(task=task)
