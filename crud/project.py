from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from crud.user import get_user_by_id
from exceptions import OwnerNotFound
from models import Project, Task
from schemas import ProjectCreateSchema


async def create_project(
    session: AsyncSession,
    project_in: ProjectCreateSchema,
) -> Project:
    owner = await get_user_by_id(session, project_in.owner)
    if not owner:
        raise OwnerNotFound

    project = Project(
        **project_in.model_dump(exclude={"owner"}),
        owner=owner
    )
    session.add(project)
    await session.commit()
    await session.refresh(
        project,
        ("owner", "tasks")
    )

    return project


async def list_projects(
    session: AsyncSession,
    owner_id: int | None = None
) -> list[Project]:
    stmt = (
        select(Project)
        .order_by(Project.created_at.desc())
        .options(
            joinedload(Project.owner),
            selectinload(Project.tasks).selectinload(Task.assignees)
        )
    )

    if owner_id is not None:
        stmt = stmt.where(Project.owner_id == owner_id)

    result = await session.scalars(stmt)

    return list(result.all())
