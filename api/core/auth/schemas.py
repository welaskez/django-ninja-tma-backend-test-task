from ninja import Schema


class AuthResponse(Schema):
    access_token: str
    refresh_token: str
