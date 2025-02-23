import asyncio
import logging

from aiogram import Dispatcher, types
from aiogram.filters import CommandStart
from config import settings

from .utils import get_bot

bot = get_bot()
dp = Dispatcher()


@dp.message(CommandStart())
async def handle_start_cmd(message: types.Message):
    await message.answer("Приветствую")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format=settings.LOGGING_FORMAT,
        handlers=[logging.StreamHandler()],
    )
    asyncio.run(main())
