from datetime import timedelta, datetime, UTC

import jwt
from pwdlib import PasswordHash

from core import settings
from exceptions import InvalidTokenTypeError

password_hash = PasswordHash.recommended()


def verify_password(plain_password: str, hashed_password: str):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def _create_jwt_token(
    user_id: int,
    expires_delta: timedelta,
    token_type: str
):
    time_now = datetime.now(tz=UTC)

    token_data = {
        "sub": str(user_id),
        "exp": time_now + expires_delta,
        "type": token_type,
        "iat": time_now
    }

    return jwt.encode(
        token_data,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )


def create_access_token(
    user_id: int,
    expires_delta: timedelta = settings.ACCESS_TOKEN_EXPIRE_MINUTES
) -> str:
    return _create_jwt_token(
        user_id,
        expires_delta,
        "access"
    )


def create_refresh_token(
    user_id: int,
    expires_delta: timedelta = settings.ACCESS_TOKEN_EXPIRE_MINUTES
) -> str:
    return _create_jwt_token(
        user_id,
        expires_delta,
        "refresh"
    )


def decode_token(token: str, token_type: str):
    decoded_data = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])

    if decoded_data["type"] != token_type:
        raise InvalidTokenTypeError("Invalid type")

    return decoded_data
