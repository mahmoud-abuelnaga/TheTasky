# external modules
from pydantic import BaseModel, Field
from typing import Optional, Annotated
from enum import Enum
from datetime import datetime


# defintion
class Status(str, Enum):
    NOT_STARTED = "not started"
    IN_PROGRESS = "in progress"
    DONE = "done"


class TaskBase(BaseModel):
    name: str
    priority: Optional[Annotated[int, Field(ge=1, le=5)]] = None
    parentTaskID: int | None = None
    teamID: int | None = None
    assignedToID: int | None = None
    deadline: datetime | None = None


class TaskRead(TaskBase):
    id: int
    createdAt: datetime
    status: Status
    progress: int

    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    name: str | None = None
    priority: Optional[Annotated[int, Field(ge=1, le=5)]] = None
    parentTaskID: int | None = None
    deadline: datetime | None = None
    status: Status | None = None
    progress: int | None = None
    assignedToID: int | None = None


class TaskCreate(TaskBase):
    pass
