from aiogram import Router, F
from aiogram.types import ChatJoinRequest, CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from sqlalchemy import select

from database import SessionLocal
from models import User
from keyboards.inline import CHANNELS_BY_REGION, enter_channel_kb

router = Router()


# =================================================
# 1. JOIN REQUEST EVENT (AUTO APPROVE YO‘Q)
# =================================================

@router.chat_join_request()
async def handle_join_request(request: ChatJoinRequest):
    """
    User kanalga so‘rov yuborganda:
    - bot userni tekshiradi
    - lekin avtomatik approve QILMAYDI
    """

    user_id = request.from_user.id
    chat_id = request.chat.id

    async with SessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == user_id)
        )
        user = result.scalar_one_or_none()

    # ❌ Botda ro‘yxatdan o‘tmagan bo‘lsa
    if not user or not user.is_registered or not user.channel:
        await safe_decline(request)
        return

    # ❌ User tanlamagan kanalga so‘rov yuborsa
    for region_channels in CHANNELS_BY_REGION.values():
        for channel_key, channel in region_channels.items():
            if channel["chat_id"] == chat_id:
                if user.channel == channel_key:
                    # To‘g‘ri kanal — lekin HOZIRCHA approve yo‘q
                    return
                else:
                    await safe_decline(request)
                    return

    # ❌ Umuman bizga tegishli bo‘lmagan kanal bo‘lsa
    await safe_decline(request)


# =================================================
# 2. CHECK JOIN CALLBACK (ASOSIY APPROVE)
# =================================================

@router.callback_query(F.data.startswith("check_join:"))
async def check_join(call: CallbackQuery):
    channel_key = call.data.split(":", 1)[1]
    user_id = call.from_user.id

    # Kanalni topamiz
    channel = None
    for region_channels in CHANNELS_BY_REGION.values():
        if channel_key in region_channels:
            channel = region_channels[channel_key]
            break

    if not channel:
        await call.answer("❌ Kanal topilmadi", show_alert=True)
        return

    try:
        await call.bot.approve_chat_join_request(
            chat_id=channel["chat_id"],
            user_id=user_id
        )

        # ✅ MATNDA LINK YO‘Q — FAQAT INLINE BUTTON
        await call.message.edit_text(
            "✅ Siz kanalga qabul qilindingiz!\n\n"
            "👇 Kanalga kirish uchun tugmani bosing",
            reply_markup=enter_channel_kb(channel_key)
        )

    except TelegramBadRequest:
        await call.answer(
            "❗ Avval kanalga so‘rov yuboring",
            show_alert=True
        )


# =================================================
# SAFE DECLINE
# =================================================

async def safe_decline(request: ChatJoinRequest):
    try:
        await request.decline()
    except TelegramBadRequest as e:
        # Ba’zi holatlarda Telegram bu xatoni tashlaydi — e’tibor bermaymiz
        if "HIDE_REQUESTER_MISSING" in str(e):
            return
        raise
