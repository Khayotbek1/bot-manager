import asyncio
from handlers import join_request

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN
from database import engine, Base

from handlers import (
    start,
    registration,
    join_request,
    admin,
    channel_events,
    chat_member
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

    # 🔹 DB yaratish
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("✅ Bot ishga tushdi")

    await dp.start_polling(
        bot,
        drop_pending_updates=True
    )


if __name__ == "__main__":
    asyncio.run(main())
