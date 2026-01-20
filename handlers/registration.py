from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select

from database import SessionLocal
from models import User
from states import RegisterState
from keyboards.reply import phone_kb, main_menu
from keyboards.inline import (
    regions_kb,
    channels_by_region_kb,
    join_channel_kb
)

router = Router()


@router.message(F.text == "📝 Ro'yxatdan o'tish")
async def start_register(message: Message, state):
    sent = await message.answer(
        "Telefon raqam jo'natish uchun pastdagi tugmani bosing.",
        reply_markup=phone_kb()
    )
    await state.update_data(last_msg_id=sent.message_id)
    await state.set_state(RegisterState.phone)


@router.message(RegisterState.phone, F.contact)
async def get_phone(message: Message, state):
    data = await state.get_data()
    await message.bot.delete_message(message.chat.id, data["last_msg_id"])

    async with SessionLocal() as session:
        user = (await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )).scalar_one_or_none()

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

    sent = await message.answer("Ismingizni kiriting:")
    await state.update_data(last_msg_id=sent.message_id)
    await state.set_state(RegisterState.first_name)


@router.message(RegisterState.first_name)
async def get_name(message: Message, state):
    data = await state.get_data()
    await message.bot.delete_message(message.chat.id, data["last_msg_id"])

    async with SessionLocal() as session:
        user = (await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )).scalar_one()

        user.first_name = message.text
        await session.commit()

    sent = await message.answer(
        "Qaysi viloyatdansiz?",
        reply_markup=regions_kb()
    )
    await state.update_data(last_msg_id=sent.message_id)
    await state.set_state(RegisterState.region)


@router.callback_query(RegisterState.region)
async def get_region(call: CallbackQuery, state):
    await call.message.delete()

    async with SessionLocal() as session:
        user = (await session.execute(
            select(User).where(User.telegram_id == call.from_user.id)
        )).scalar_one()

        user.region = call.data
        await session.commit()

    await call.message.answer(
        "Hududingizdagi Smartlife kanallari",
        reply_markup=channels_by_region_kb(call.data)
    )
    await state.set_state(RegisterState.channel)


@router.callback_query(RegisterState.channel, F.data.startswith("channel:"))
async def get_channel(call: CallbackQuery, state):
    await call.message.delete()

    channel_key = call.data.split(":")[1]

    async with SessionLocal() as session:
        user = (await session.execute(
            select(User).where(User.telegram_id == call.from_user.id)
        )).scalar_one()

        user.channel = channel_key
        user.is_registered = True
        await session.commit()

    await call.message.answer(
        "✅ Siz ro'yxatdan o'tdingiz!\n"
        "Endi kanalga kirishingiz mumkin 👇",
        reply_markup=join_channel_kb(channel_key)
    )

    await call.message.answer(
        "🏠 Bosh menu",
        reply_markup=main_menu()
    )

    await state.clear()
