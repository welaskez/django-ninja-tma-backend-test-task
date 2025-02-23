from aiogram import Bot
from config import settings


def get_bot() -> Bot:
    return Bot(token=settings.BOT_TOKEN)
