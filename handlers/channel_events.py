from aiogram import Router
from aiogram.types import ChatMemberUpdated
from sqlalchemy import select
from datetime import datetime
from zoneinfo import ZoneInfo

from database import SessionLocal
from models import User
from keyboards.inline import ALL_CHANNEL_IDS

router = Router()
UZ_TZ = ZoneInfo("Asia/Tashkent")


@router.chat_member()
async def handle_channel_member(event: ChatMemberUpdated):
    if event.chat.id not in ALL_CHANNEL_IDS:
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

        now = datetime.utcnow()  # ✅ TZ YO‘Q

        # ➕ Kanalga kirdi
        if old_status in ("left", "kicked") and new_status in ("member", "administrator"):
            user.joined_at = now
            user.left_at = None

        # ➖ Kanaldan chiqdi
        elif old_status in ("member", "administrator") and new_status in ("left", "kicked"):
            user.left_at = now

        await session.commit()
