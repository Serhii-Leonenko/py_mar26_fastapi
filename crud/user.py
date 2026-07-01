from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from schemas.user import UserCreateSchema


async def get_all_users(db: AsyncSession) -> list[User]:
    result = await db.scalars(select(User))

    return list(result.all())


async def create_user(db: AsyncSession, user_data: UserCreateSchema) -> User:
    user = User(**user_data.model_dump())
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    return await db.scalar(select(User).where(User.email == email))


async def get_user_by_id(db: AsyncSession, owner_id: int) -> User | None:
    return await db.scalar(select(User).where(User.id == owner_id))
