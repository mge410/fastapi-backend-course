from enum import Enum

from pydantic import BaseModel


class TaskStatus(str, Enum):
    NEW = "new"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"


class TaskCreateData(BaseModel):
    title: str
    description: str
    status: TaskStatus = TaskStatus.NEW


class TaskUpdateData(BaseModel):
    title: str
    description: str
    status: TaskStatus = TaskStatus.NEW


class TaskData(BaseModel):
    id: int
    title: str
    description: str
    advice_by_ai: str
    status: TaskStatus = TaskStatus.NEW
