from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from __init__ import setup, schedule

import asyncio

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.MARKDOWN)

dp = Dispatcher()


async def main() -> None:
    setup(dp)
    schedule()

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
