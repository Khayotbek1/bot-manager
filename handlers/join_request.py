from aiogram import Router
from aiogram.types import ChatJoinRequest
from aiogram.exceptions import TelegramBadRequest
from sqlalchemy import select

from database import SessionLocal
from models import User
from keyboards.inline import CHANNELS_BY_REGION

router = Router()


@router.chat_join_request()
async def handle_join_request(request: ChatJoinRequest):
    user_id = request.from_user.id
    chat_id = request.chat.id

    async with SessionLocal() as session:
        user = (
            await session.execute(
                select(User).where(User.telegram_id == user_id)
            )
        ).scalar_one_or_none()

    # ❌ Botda ro‘yxatdan o‘tmagan yoki kanal tanlanmagan
    if not user or not user.is_registered or not user.channel:
        await safe_decline(request)
        return

    # 🔍 User tanlagan kanal haqiqatan shu kanalmi?
    allowed = False

    for region_channels in CHANNELS_BY_REGION.values():
        for channel_key, channel in region_channels.items():
            if (
                channel["chat_id"] == chat_id
                and user.channel == channel_key
            ):
                allowed = True
                break

    if allowed:
        await safe_approve(request)
    else:
        await safe_decline(request)




async def safe_approve(request: ChatJoinRequest):
    try:
        await request.approve()
    except TelegramBadRequest as e:
        if "HIDE_REQUESTER_MISSING" in str(e):
            pass
        else:
            raise


async def safe_decline(request: ChatJoinRequest):
    try:
        await request.decline()
    except TelegramBadRequest as e:
        if "HIDE_REQUESTER_MISSING" in str(e):
            pass
        else:
            raise
