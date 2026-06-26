from pydantic import BaseModel, ConfigDict
from models.task import TaskStatus
from schemas import UserReadSchema


class TaskCreateSchema(BaseModel):
    title: str
    description: str
    assignees: list[int]


class TaskReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    status: TaskStatus
    assignees: list[UserReadSchema]


class TaskUpdateSchema(BaseModel):
    status: TaskStatus
    assignees: list[int]

