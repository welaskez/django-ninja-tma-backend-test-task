import asyncio

from aiogram.enums import ChatMemberStatus
from bot.utils import get_bot


async def check_telegram_subscribe(link: str, tg_id: int) -> bool:
    channel_username = f"@{link.split('/')[-1]}"
    bot = get_bot()

    for _ in range(3):
        chat_member = await bot.get_chat_member(chat_id=channel_username, user_id=tg_id)
        if chat_member.status not in (ChatMemberStatus.KICKED, ChatMemberStatus.LEFT):
            await bot.session.close()
            return True
        else:
            await asyncio.sleep(1)

    await bot.session.close()
    return False
