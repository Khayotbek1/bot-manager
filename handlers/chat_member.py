from aiogram import Router
from aiogram.types import ChatMemberUpdated
from datetime import datetime
from sqlalchemy import select

from database import SessionLocal
from models import User
from keyboards.inline import CHANNELS_BY_REGION

router = Router()


def is_tracked_channel(chat_id: int, user_channel_key: str) -> bool:
    for region_channels in CHANNELS_BY_REGION.values():
        for key, channel in region_channels.items():
            if key == user_channel_key and channel["chat_id"] == chat_id:
                return True
    return False


@router.chat_member()
async def handle_chat_member(update: ChatMemberUpdated):
    if update.chat.type != "channel":
        return

    old = update.old_chat_member.status
    new = update.new_chat_member.status

    member = update.new_chat_member.user
    user_id = member.id
    chat_id = update.chat.id

    async with SessionLocal() as session:
        user = (
            await session.execute(
                select(User).where(User.telegram_id == user_id)
            )
        ).scalar_one_or_none()

        if not user or not user.channel:
            return

        if not is_tracked_channel(chat_id, user.channel):
            return

        # ❌ chiqib ketdi
        if old == "member" and new in ("left", "kicked"):
            user.left_at = datetime.utcnow()
            await session.commit()
            return

        # ✅ qayta kirdi
        if old in ("left", "kicked") and new == "member":
            user.left_at = None
            await session.commit()
            return
