from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict, Field


class UserCreateSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str = Field(min_length=8)


class UserReadSchema(BaseModel):
    id: int
    full_name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenRefreshSchema(BaseModel):
    refresh_token: str
