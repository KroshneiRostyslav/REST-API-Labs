from datetime import datetime, timedelta, UTC
from typing import Optional

from jose import jwt, JWTError
from fastapi import HTTPException, status

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
):
    to_encode = data.copy()

    expire = (
        datetime.now(UTC)
        + (
            expires_delta
            or timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            )
        )
    )

    to_encode.update(
        {
            "exp": expire,
            "type": "access"
        }
    )

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def create_refresh_token(
    data: dict
):
    to_encode = data.copy()

    expire = (
        datetime.now(UTC)
        + timedelta(
            days=REFRESH_TOKEN_EXPIRE_DAYS
        )
    )

    to_encode.update(
        {
            "exp": expire,
            "type": "refresh"
        }
    )

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def verify_token(
    token: str,
    token_type: str
):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        if payload.get("type") != token_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )