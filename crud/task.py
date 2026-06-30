from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from exceptions import AssigneeNotFound, ProjectNotFound, TaskNotFound
from models import Task, User, Project
from schemas import TaskCreateSchema, TaskUpdateSchema


async def get_task_by_id(
    session: AsyncSession,
    task_id: int,
) -> Task | None:
    stmt = (
        select(Task)
        .where(Task.id == task_id)
        .options(selectinload(Task.assignees))
    )

    return await session.scalar(stmt)


async def _get_assignees_by_ids(
    session: AsyncSession,
    assignee_ids: list[int],
) -> list[User]:
    if not assignee_ids:
        return []

    result = await session.scalars(
        select(User).where(User.id.in_(assignee_ids))
    )
    assignees = list(result.all())

    assignees_from_db = [assignee.id for assignee in assignees]
    not_found_assignees = set(assignee_ids) - set(assignees_from_db)

    if not_found_assignees:
        raise AssigneeNotFound(list(not_found_assignees))

    return assignees


async def create_task(
    session: AsyncSession,
    task_in: TaskCreateSchema,
) -> Task:
    project = await session.get(Project, task_in.project)
    if not project:
        raise ProjectNotFound

    assignees = await _get_assignees_by_ids(session, task_in.assignees)
    task = Task(
        **task_in.model_dump(exclude={"assignees", "project"}),
        project=project,
        assignees=assignees,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task, ("assignees",))

    return task


async def update_task(
    session: AsyncSession,
    task_id: int,
    task_in: TaskUpdateSchema,
) -> Task:
    task = await get_task_by_id(session, task_id)
    if not task:
        raise TaskNotFound

    task.status = task_in.status
    task.assignees = await _get_assignees_by_ids(session, task_in.assignees)
    await session.commit()
    await session.refresh(task, ("assignees",))

    return task


async def delete_task(
    session: AsyncSession,
    task_id: int,
) -> None:
    task = await get_task_by_id(session, task_id)
    if not task:
        raise TaskNotFound

    await session.delete(task)
    await session.commit()
