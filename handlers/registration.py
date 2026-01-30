from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from sqlalchemy import select
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter


from database import SessionLocal
from models import User
from states import RegisterState
from keyboards.reply import (
    phone_kb,
    main_menu,
    back_step_kb
)
from keyboards.inline import (
    regions_kb,
    channels_by_region_kb,
    join_channel_kb,
    check_join_kb
)

router = Router()


# =========================
# START REGISTRATION
# =========================

@router.message(F.text == "📝 Ro'yxatdan o'tish")
async def start_register(message: Message, state):
    await state.clear()

    await message.answer(
        "📱 Telefon raqam jo'natish uchun pastdagi tugmani bosing.",
        reply_markup=phone_kb()
    )
    await state.set_state(RegisterState.phone)


# =========================
# BACK STEP (1 QADAM ORQAGA)
# =========================

@router.message(
    StateFilter(
        RegisterState.phone,
        RegisterState.first_name,
        RegisterState.region,
        RegisterState.channel,
    ),
    F.text == "⬅️ Ortga"
)
async def back_step(message: Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state == RegisterState.channel:
        await state.set_state(RegisterState.region)
        await message.answer(
            "📍 Qaysi viloyatdansiz?",
            reply_markup=regions_kb()
        )

    elif current_state == RegisterState.region:
        await state.set_state(RegisterState.first_name)
        await message.answer(
            "✍️ Ismingizni kiriting:",
            reply_markup=back_step_kb()
        )

    elif current_state == RegisterState.first_name:
        await state.set_state(RegisterState.phone)
        await message.answer(
            "📱 Telefon raqam jo'natish uchun pastdagi tugmani bosing.",
            reply_markup=phone_kb(),
        )


# =========================
# GET PHONE
# =========================

@router.message(RegisterState.phone, F.contact)
async def get_phone(message: Message, state):
    async with SessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()

        if not user:
            user = User(
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                phone=message.contact.phone_number
            )
            session.add(user)
        else:
            user.phone = message.contact.phone_number

        await session.commit()

    await message.answer(
        "✍️ Ismingizni kiriting:",
        reply_markup=back_step_kb()
    )
    await state.set_state(RegisterState.first_name)


# =========================
# GET NAME
# =========================

@router.message(RegisterState.first_name)
async def get_name(message: Message, state):
    async with SessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = result.scalar_one()

        user.first_name = message.text.strip()
        await session.commit()

    await message.answer(
        "📍 Qaysi viloyatdansiz?",
        reply_markup=regions_kb()
    )
    await state.set_state(RegisterState.region)


# =========================
# GET REGION
# =========================

@router.callback_query(RegisterState.region)
async def get_region(call: CallbackQuery, state):
    await call.message.delete()

    async with SessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == call.from_user.id)
        )
        user = result.scalar_one()

        user.region = call.data
        await session.commit()

    await call.message.answer(
        "📢 Smartlife kanallari 👇",
        reply_markup=channels_by_region_kb(call.data)
    )
    await call.message.answer(
        "⬅️ Ortga",
        reply_markup=back_step_kb()
    )
    await state.set_state(RegisterState.channel)


# =========================
# GET CHANNEL
# =========================

@router.callback_query(RegisterState.channel, F.data.startswith("channel:"))
async def get_channel(call: CallbackQuery, state):
    await call.message.delete()

    channel_key = call.data.split(":", 1)[1]

    async with SessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == call.from_user.id)
        )
        user = result.scalar_one()

        user.channel = channel_key
        user.is_registered = True
        await session.commit()

    # 1️⃣ Kanalga so‘rov yuborish
    await call.message.answer(
        "📌 Kanalga kirish uchun:\n\n"
        "1️⃣ Avval kanalga so‘rov yuboring\n"
        "2️⃣ Keyin «Tekshirish» tugmasini bosing",
        reply_markup=join_channel_kb(channel_key)
    )

    # 2️⃣ Tekshirish
    await call.message.answer(
        "👇 So‘rov yuborgach tekshiring",
        reply_markup=check_join_kb(channel_key)
    )

    # 3️⃣ Navigatsiya (FSM SAQLANADI)
    await call.message.answer(
        "📍 Keyingi amalni tanlang:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🏠 Bosh menu")],
                [KeyboardButton(text="⬅️ Ortga")]
            ],
            resize_keyboard=True
        )
    )
    await state.set_state(RegisterState.channel)


