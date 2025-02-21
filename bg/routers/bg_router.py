from typing import Annotated

from faststream.rabbit import RabbitRouter
from faststream import Depends

from logger_config import logger
from schemas import BgTask, BgTasks
from bg.services.workers import BgWorker
from bg.config import broker

router = RabbitRouter()


@router.publisher('sender')
@router.subscriber("pinger")
async def ping(
        # task
        service: Annotated[BgTasks, Depends(BgWorker().pinger)]
):
    # logger.debug(task)
    logger.debug('bg/router/bg_router: def ping')
    return service


@router.publisher('worker')
@router.subscriber("sender")
async def send(
        tasks: Annotated[BgTasks, Depends(BgWorker().sender)]
):
    for task in tasks.names:
        logger.debug(task)
        await broker.publish(queue='worker', message=task)


@router.subscriber("worker")
async def send(
        task: str
):
    return await BgWorker().worker(task=task)
