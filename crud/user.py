from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import get_password_hash, verify_password
from models import User
from schemas.user import UserCreateSchema


async def get_all_users(db: AsyncSession) -> list[User]:
    result = await db.scalars(select(User))

    return list(result.all())


async def create_user(db: AsyncSession, user_data: UserCreateSchema) -> User:
    hashed_password = get_password_hash(user_data.password)

    user = User(
        **user_data.model_dump(exclude={"password"}),
        hashed_password=hashed_password
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    return await db.scalar(select(User).where(User.email == email))


async def get_user_by_id(db: AsyncSession, owner_id: int) -> User | None:
    return await db.scalar(select(User).where(User.id == owner_id))


async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
    user = await get_user_by_email(db, email)
    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user
