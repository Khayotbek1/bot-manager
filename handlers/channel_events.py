from aiogram import Router
from aiogram.types import ChatMemberUpdated
from sqlalchemy import select
from datetime import datetime
from zoneinfo import ZoneInfo

from database import SessionLocal
from models import User
from config import CHANNEL_ID  # -100xxxxxxxxx

router = Router()
UZ_TZ = ZoneInfo("Asia/Tashkent")


@router.chat_member()
async def handle_channel_member(event: ChatMemberUpdated):
    # ❗ Faqat kanalni tekshiramiz
    if event.chat.id != CHANNEL_ID:
        return

    user_id = event.new_chat_member.user.id

    old_status = event.old_chat_member.status
    new_status = event.new_chat_member.status

    async with SessionLocal() as session:
        user = (await session.execute(
            select(User).where(User.telegram_id == user_id)
        )).scalar_one_or_none()

        if not user:
            return

        # ➕ Kanalga kirdi
        if old_status in ("left", "kicked") and new_status in ("member", "administrator"):
            user.joined_at = datetime.now(UZ_TZ)
            user.left_at = None

        # ➖ Kanaldan chiqdi
        elif old_status in ("member", "administrator") and new_status in ("left", "kicked"):
            user.left_at = datetime.now(UZ_TZ)

        await session.commit()
