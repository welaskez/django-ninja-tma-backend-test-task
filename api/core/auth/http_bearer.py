import jwt
from django.shortcuts import get_object_or_404
from ninja.errors import HttpError
from ninja.security import HttpBearer
from users.models import User

from core.auth.jwt import decode_jwt
from core.auth.schemas import TokenInfo


class TelegramAuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = TokenInfo.model_validate(decode_jwt(token))
            user = get_object_or_404(User, id=payload.sub)
            return user
        except jwt.ExpiredSignatureError:
            raise HttpError(status_code=401, message="Token has expired")
        except jwt.InvalidTokenError:
            raise HttpError(status_code=401, message="Invalid token")
