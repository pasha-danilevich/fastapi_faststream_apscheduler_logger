from datetime import timedelta, datetime
from enum import StrEnum
from typing import Any, Annotated, Union, Literal


from pydantic import BaseModel, ConfigDict, Field


class BgTaskBase(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    task_id: str = "1"
    source: str = "api"
    load_type: str = "import"
    start_date: datetime = datetime.now()
    end_date: datetime = datetime.now()


class BgTasks(BaseModel):
    names: list = ["mss", "kvs"]


class BgTask(BaseModel):
    name: str = "mss"


class Cron(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    trigger_type: Literal["cron"]
    year: int = None
    month: int = None
    day: int = None
    week: int = None
    day_of_week: int = None
    hour: int = None
    minute: int = None
    second: int = None
    start_date: datetime = datetime.now()
    end_date: datetime = None
    timezone: str = "Europe/Moscow"
    # aps: CronTrigger = Field(default=None, exclude=True)


class Interval(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    trigger_type: Literal["interval"]
    weeks: int = 0
    days: int = 0
    hours: int = 0
    minutes: int = 0
    seconds: int = 0
    start_date: datetime = datetime.now()
    end_date: datetime = None
    timezone: str = "Europe/Moscow"
    # aps: IntervalTrigger = Field(default=None, exclude=True)


class BgJob(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: str = "1"
    name: str = "mss"
    trigger: Annotated[
        Union[
            Cron,
            Interval,
        ],
        Field(..., discriminator="trigger_type"),
    ]  # CronTrigger | IntervalTrigger = IntervalTrigger(seconds=5)
    tasks: BgTasks


class BgJobResponse(BaseModel):
    id: str
    name: str
    trigger: Any
    next_run_time: str
