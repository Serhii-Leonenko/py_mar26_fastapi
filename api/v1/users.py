from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from crud.user import get_all_users, create_user, get_user_by_email
from db.session import get_db
from schemas import UserCreateSchema, UserReadSchema


router = APIRouter(tags=["users"], prefix="/users")


@router.get("/", response_model=list[UserReadSchema])
async def get_users(db: Annotated[AsyncSession, Depends(get_db)]):
    return await get_all_users(db)
