from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from crud.users import get_all_users, create_user, get_user_by_email
from db.session import get_db
from schemas import UserCreateSchema, UserReadSchema


app = FastAPI()


@app.get("/users/", response_model=list[UserReadSchema])
async def get_users(db: Annotated[AsyncSession, Depends(get_db)]):
    return await get_all_users(db)


@app.post("/users/", response_model=UserReadSchema)
async def create_new_user(
    user_data: UserCreateSchema,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    if await get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    return await create_user(db, user_data)
