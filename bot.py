import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN
from database import engine

from handlers import (
    start,
    registration,
    join_request,
    admin,
    channel_events,
    chat_member,
)


async def main():
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )

    dp = Dispatcher()

    # 🔹 Routerlar
    dp.include_router(start.router)
    dp.include_router(registration.router)
    dp.include_router(join_request.router)
    dp.include_router(channel_events.router)
    dp.include_router(chat_member.router)
    dp.include_router(admin.router)

    print("✅ Bot ishga tushdi")

    try:
        await dp.start_polling(
            bot,
            drop_pending_updates=True
        )
    finally:
        # 🔹 Toza shutdown
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
