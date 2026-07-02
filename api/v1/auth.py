import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.security import create_access_token, create_refresh_token, decode_token
from crud.user import get_user_by_email, create_user, authenticate_user, get_user_by_id
from db.session import get_db
from schemas import UserReadSchema, UserCreateSchema
from schemas.user import UserLoginSchema, TokenResponseSchema, TokenRefreshSchema

router = APIRouter(prefix="/auth", tags=["auth"])


logger = logging.getLogger(__name__)


@router.post("/register", response_model=UserReadSchema)
async def register(
    user_data: UserCreateSchema,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    existing_user = await get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Email already registered"
        )

    return await create_user(db, user_data=user_data)


@router.post("/login", response_model=TokenResponseSchema)
async def login(
    login_date: UserLoginSchema,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    user = await authenticate_user(
        db=db,
        email=login_date.email,
        password=login_date.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    return TokenResponseSchema(
        access_token=create_access_token(user_id=user.id),
        refresh_token=create_refresh_token(user_id=user.id)
    )


@router.post("/refresh", response_model=TokenResponseSchema)
async def refresh(
    refresh_token_data: TokenRefreshSchema,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    try:
        decoded_data = decode_token(
            token=refresh_token_data.refresh_token,
            token_type="refresh"
        )
    except Exception as error:
        logger.error(error)

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user_id = int(decoded_data.get("sub"))

    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    return TokenResponseSchema(
        access_token=create_access_token(user_id=user_id),
        refresh_token=refresh_token_data.refresh_token
    )
