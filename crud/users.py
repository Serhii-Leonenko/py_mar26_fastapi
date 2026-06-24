from sqlalchemy import select
from sqlalchemy.orm import Session
from models import User
from schemas.users import UserCreateSchema


def get_all_users(
    db: Session
) -> list[User]:
    return list(
        db.scalars(select(User)).all()
    )


def create_user(
    db: Session,
    user_data: UserCreateSchema
) -> User:
    user = User(**user_data.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user_by_email(
    db: Session,
    email: str
) -> User | None:
    return db.scalar(select(User).where(User.email == email))
