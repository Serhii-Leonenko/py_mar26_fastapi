from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from crud.users import get_all_users, create_user, get_user_by_email
from db.session import get_db
from schemas import UserCreateSchema, UserReadSchema


app = FastAPI()


@app.get("/users/", response_model=list[UserReadSchema])
def get_users(db: Annotated[Session, Depends(get_db)]):
    return get_all_users(db)


@app.post("/users/", response_model=UserReadSchema)
def create_new_user(
    user_data: UserCreateSchema,
    db: Annotated[Session, Depends(get_db)]
):
    if get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    return create_user(db, user_data)
