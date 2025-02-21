import asyncio
import datetime

from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from faststream.rabbit import RabbitBroker

from bg.config import scheduler, broker_session
from logger_config import logger
from schemas import BgJob, BgJobResponse, BgTasks


class Scheduler:

    def __init__(self):
        self.scheduler: AsyncIOScheduler = scheduler

    def scheduler_start(self) -> None:
        self.scheduler.start()

    def scheduler_stop(self):
        self.scheduler_remove_all_jobs()
        self.scheduler.shutdown()

    def scheduler_add_job(self, job: BgJob) -> BgJobResponse:
        logger.debug("Запуск работы")
        trigger_dict = job.trigger.model_dump(
            exclude_none=True, exclude_unset=True, exclude={"trigger_type"}
        )
        self.scheduler.add_job(
            id=job.id,
            kwargs=job.tasks.model_dump(),
            name=job.name,
            func=Scheduler.export_tasks,
            trigger=(
                IntervalTrigger(**trigger_dict)
                if job.trigger.trigger_type == "interval"
                else CronTrigger(**trigger_dict)
            ),
            replace_existing=True,
        )
        logger.debug(f"Добавлено задание, {job.name}")
        return self.scheduler_get_job_by_id(job_id=job.id)

    def scheduler_remove_job(self, job_id):
        job = self.scheduler_get_job_by_id(job_id)
        if not job:
            return None
        self.scheduler.remove_job(job_id=job_id)
        return {"job_id": job.id, "deleted": True}

    def scheduler_get_jobs(self) -> list[BgJobResponse]:
        jobs = self.scheduler.get_jobs(pending=True)
        job_list = []
        for job in jobs:
            bg_job_response = BgJobResponse(
                id=job.id,
                name=job.name,
                trigger=str(job.trigger),
                next_run_time=str(job.next_run_time),
            )
            job_list.append(bg_job_response)

        return job_list

    def scheduler_remove_all_jobs(self):
        jobs = self.scheduler_get_jobs()
        if len(jobs) > 0:
            for job in jobs:
                self.scheduler_remove_job(job_id=job.id)

    def scheduler_get_job_by_id(self, job_id) -> BgJobResponse | dict:
        try:
            job = self.scheduler.get_job(job_id=job_id)
            return BgJobResponse(
                id=job.id,
                name=job.name,
                trigger=str(job.trigger),
                next_run_time=str(job.next_run_time),
            )
        except:
            return {"job_id": job_id, "not found": True}

    @staticmethod
    @broker_session
    async def export_tasks(bg: RabbitBroker, **task):
        task = BgTasks(**task)
        logger.info(f"Я работаю... {datetime.datetime.now()}, {task.names}")
        res = await bg.publish(message=task, queue="pinger")

    @staticmethod
    async def scheduler_lifespan(app):
        scheduler = Scheduler()
        try:
            scheduler.scheduler_start()
            logger.debug("Планировщик запущен")
            yield
        except Exception as e:
            logger.debug(f"Ошибка запуска планировщика {e}")
        finally:
            scheduler.scheduler_stop()
            logger.debug("Планировщик остановлен")


print
