from ninja import Schema

from core.auth.enums import TokenType


class TokenInfo(Schema):
    sub: str
    exp: int
    iat: int
    type: TokenType


class AuthBody(Schema):
    query_str: str


class RefreshBody(Schema):
    refresh_token: str


class AuthResponse(Schema):
    access_token: str
    refresh_token: str
