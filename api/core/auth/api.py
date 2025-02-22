from ninja.errors import HttpError
from ninja.router import Router
from pydantic import ValidationError
from users.models import User

from .enums import TokenType
from .jwt import decode_jwt, get_tokens
from .schemas import AuthBody, AuthResponse, RefreshBody, TokenInfo
from .utils import validate_init_data

router = Router()


@router.post("", response=AuthResponse)
def auth(request, body: AuthBody):
    init_data = validate_init_data(query_str=body.query_str)

    user, created = User.objects.get_or_create(
        tg_id=init_data.user.id,
        username=init_data.user.username or "temp",
        photo=init_data.user.photo_url,
    )

    if created and not init_data.user.username:
        user.username = f"Player#N{user.id}"
        user.save()

    return get_tokens(sub=str(user.id))


@router.post(path="/refresh", response=AuthResponse)
def refresh_tokens(request, body: RefreshBody):
    try:
        payload = TokenInfo.model_validate(decode_jwt(body.refresh_token))
    except ValidationError:
        raise HttpError(status_code=401, message="Invalid token")
    if payload.type == TokenType.REFRESH:
        return get_tokens(sub=payload.sub)

    raise HttpError(status_code=401, message="Invalid token type")
