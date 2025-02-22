from aiogram.utils.web_app import WebAppInitData, safe_parse_webapp_init_data
from config import settings
from ninja.errors import AuthenticationError


def validate_init_data(query_str: str) -> WebAppInitData:
    try:
        init_data = safe_parse_webapp_init_data(
            token=settings.BOT_TOKEN,
            init_data=query_str,
        )
    except ValueError:
        raise AuthenticationError

    return init_data
