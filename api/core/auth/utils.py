from aiogram.utils.web_app import WebAppInitData, safe_parse_webapp_init_data
from config import settings
from ninja.errors import HttpError


def validate_init_data(query_str: str) -> WebAppInitData:
    try:
        init_data = safe_parse_webapp_init_data(
            token=settings.BOT_TOKEN,
            init_data=query_str,
        )
    except ValueError:
        raise HttpError(status_code=401, message="Invalid query string")

    return init_data
