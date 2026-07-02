from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from crud.task import create_task, update_task, delete_task
from db.session import get_db
from schemas import TaskCreateSchema, TaskReadSchema, TaskUpdateSchema
from exceptions import ProjectNotFound, TaskNotFound, AssigneeNotFound


router = APIRouter(tags=["tasks"], prefix="/task")


@router.post("/", response_model=TaskReadSchema, status_code=status.HTTP_201_CREATED)
async def create_new_task(
    task_data: TaskCreateSchema,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    try:
        return await create_task(db, task_data)
    except (ProjectNotFound, AssigneeNotFound) as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(error)
        )


@router.put("/{task_id}", response_model=TaskReadSchema)
async def update_task(
    task_id: int,
    task_data: TaskUpdateSchema,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    try:
        return await update_task(session=db, task_in=task_data, task_id=task_id)
    except TaskNotFound as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )
    except AssigneeNotFound as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(error)
        )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    try:
        return await delete_task(session=db, task_id=task_id)
    except TaskNotFound as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )
