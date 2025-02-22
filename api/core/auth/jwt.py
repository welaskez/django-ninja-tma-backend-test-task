from datetime import datetime, timedelta, timezone

import jwt
from config import settings

from .enums import TokenType
from .schemas import AuthResponse


def encode_jwt(
    payload: dict,
    private_key: str = settings.PRIVATE_KEY_PATH.read_text(),
    algorithm: str = settings.ALGORITHM,
    expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    expire_timedelta: timedelta | None = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(exp=expire, iat=now)
    return jwt.encode(payload=to_encode, key=private_key, algorithm=algorithm)


def decode_jwt(
    token: str,
    public_key: str = settings.PUBLIC_KEY_PATH.read_text(),
    algorithm: str = settings.ALGORITHM,
):
    return jwt.decode(jwt=token, key=public_key, algorithms=[algorithm])


def get_tokens(sub: str) -> AuthResponse:
    access_token = encode_jwt(payload={"sub": sub, "type": TokenType.ACCESS})
    refresh_token = encode_jwt(
        payload={"sub": sub, "type": TokenType.REFRESH},
        expire_timedelta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )

    return AuthResponse(access_token=access_token, refresh_token=refresh_token)
