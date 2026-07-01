from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from crud.project import list_projects, create_project
from db.session import get_db
from exceptions import OwnerNotFound
from schemas import ProjectReadSchema, ProjectCreateSchema

router = APIRouter(tags=["projects"], prefix="/projects")


@router.get("/", response_model=list[ProjectReadSchema])
async def get_projects(db: Annotated[AsyncSession, Depends(get_db)], owner_id: int | None = None):
    return await list_projects(db, owner_id)


@router.post("/", response_model=ProjectReadSchema)
async def create_new_project(
    project_data: ProjectCreateSchema,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    try:
        return await create_project(db, project_data)
    except OwnerNotFound as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(error)
        )
