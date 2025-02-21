import logging
from typing import Annotated, Union


import uvicorn
from fastapi import FastAPI, Depends
from bg.services.schedulers import Scheduler, BgJobResponse
from logger_config import logger

app = FastAPI(lifespan=Scheduler.scheduler_lifespan)


@app.post("/add_job")
async def run_job(
    service: Annotated[BgJobResponse, Depends(Scheduler().scheduler_add_job)],
) -> BgJobResponse:
    return service


@app.get("/get_jobs")
async def get_jobs(
    service: Annotated[list[BgJobResponse], Depends(Scheduler().scheduler_get_jobs)],
) -> list[BgJobResponse]:
    logger.info(f"get_jobs service: {service}")
    return service


@app.get("/get_job")
async def get_job(
    service: Annotated[BgJobResponse, Depends(Scheduler().scheduler_get_job_by_id)],
) -> BgJobResponse:
    return service


@app.post("/remove_job")
async def remove_job(
    service: Annotated[dict, Depends(Scheduler().scheduler_remove_job)],
):
    return service


def run_api():
    uvicorn.run(app, port=8009)
