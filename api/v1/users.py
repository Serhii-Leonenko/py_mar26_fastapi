from typing import Annotated

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from crud.user import get_all_users
from db.session import get_db
from schemas import UserReadSchema


router = APIRouter(tags=["users"], prefix="/users")


@router.get("/", response_model=list[UserReadSchema])
async def get_users(db: Annotated[AsyncSession, Depends(get_db)]):
    return await get_all_users(db)
