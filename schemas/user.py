from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreateSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str


class UserReadSchema(BaseModel):
    id: int
    full_name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
