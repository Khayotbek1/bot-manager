from aiogram import Router
from aiogram.types import ChatJoinRequest
from aiogram.exceptions import TelegramNetworkError
from sqlalchemy import select

from database import SessionLocal
from models import User

router = Router()


@router.chat_join_request()
async def handle_join(event: ChatJoinRequest):
    async with SessionLocal() as session:
        user = (await session.execute(
            select(User).where(User.telegram_id == event.from_user.id)
        )).scalar_one_or_none()

    # Agar user ro‘yxatdan o‘tmagan bo‘lsa
    if not user or not user.is_registered:
        try:
            await event.bot.send_message(
                event.from_user.id,
                "❗ Kanalga kirish uchun avval botda ro‘yxatdan o‘ting."
            )
        except TelegramNetworkError:
            pass
        return

    # Agar ro‘yxatdan o‘tgan bo‘lsa → approve
    try:
        await event.approve()
    except TelegramNetworkError:
        # Network yo‘q → jim o‘tamiz (bot yiqilmaydi)
        pass
