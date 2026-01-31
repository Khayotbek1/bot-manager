from aiogram import Router, F
from aiogram.types import ChatJoinRequest, CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from sqlalchemy import select

from database import SessionLocal
from models import User
from keyboards.inline import CHANNELS_BY_REGION, enter_channel_kb

router = Router()



@router.chat_join_request()
async def handle_join_request(request: ChatJoinRequest):
    """
    UNIVERSAL JOIN REQUEST HANDLER

    - Qaysi linkdan kirganidan qat’i nazar
    - HAR DOIM avtomatik approve
    - Kick / ban YO‘Q
    - Faqat botdan ro‘yxatdan o‘tmaganlarga xabar yuboriladi
    """

    user_id = request.from_user.id

    # 1️⃣ HAR DOIM APPROVE
    try:
        await request.approve()
    except TelegramBadRequest:
        return

    # 2️⃣ User botda bormi — tekshiramiz
    async with SessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == user_id)
        )
        user = result.scalar_one_or_none()

    # 3️⃣ Agar botdan ro‘yxatdan o‘tmagan bo‘lsa — xabar yuboramiz
    if not user or not user.is_registered:
        try:
            await request.bot.send_message(
                user_id,
                "👋 Xush kelibsiz!\n\n"
                "📌 Botdan ro‘yxatdan o‘ting va "
                "operatorlarimiz orqali savollaringizga javob oling!"
            )
        except TelegramBadRequest:
            # user botga yozmagan bo‘lishi mumkin — jim o‘tamiz
            pass


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
