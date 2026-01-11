from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select

from database import SessionLocal
from models import User
from states import RegisterState
from keyboards.reply import phone_kb, main_menu
from keyboards.inline import regions_kb, join_channel_kb

router = Router()  # 🔴 MUHIM: router SHU YERDA E'LON QILINADI


@router.message(F.text == "📝 Ro'yxatdan o'tish")
async def start_register(message: Message, state):
    await message.answer(
        "Telefon raqam jo'natish uchun pastdagi tugmani bosing.",
        reply_markup=phone_kb()
    )
    await state.set_state(RegisterState.phone)


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
                first_name=message.from_user.first_name,
                phone=message.contact.phone_number
            )
            session.add(user)
        else:
            user.phone = message.contact.phone_number

        await session.commit()

    await message.answer("Ismingizni kiriting:")
    await state.set_state(RegisterState.first_name)


@router.message(RegisterState.first_name)
async def get_name(message: Message, state):
    async with SessionLocal() as session:
        user = (await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )).scalar_one()

        user.first_name = message.text
        await session.commit()

    await message.answer(
        "Qaysi viloyatdansiz?",
        reply_markup=regions_kb()
    )
    await state.set_state(RegisterState.region)


@router.callback_query(RegisterState.region)
async def get_region(call: CallbackQuery, state):
    async with SessionLocal() as session:
        user = (await session.execute(
            select(User).where(User.telegram_id == call.from_user.id)
        )).scalar_one()

        user.region = call.data
        user.is_registered = True
        await session.commit()

    # ✅ Ro‘yxatdan o‘tish yakuni + kanal tugmasi
    await call.message.answer(
        "✅ Siz ro'yxatdan o'tdingiz!\n"
        "Endi kanalga kirishingiz mumkin 👇",
        reply_markup=join_channel_kb()
    )

    # 🏠 Bosh menu
    await call.message.answer(
        "🏠 Bosh menu",
        reply_markup=main_menu()
    )

    await state.clear()
