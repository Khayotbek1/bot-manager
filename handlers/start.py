from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy import select
from aiogram.fsm.context import FSMContext
from keyboards.reply import start_menu_kb, main_menu_registered
from database import SessionLocal
from keyboards.reply import start_menu_kb, back_kb
from models import User

router = Router()


# =========================
# /start
# =========================

@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Assalomu alaykum! 👋\n\n"
        "Smartlife botiga xush kelibsiz.\n"
        "Quyidagi menyulardan birini tanlang:",
        reply_markup=start_menu_kb()
    )


# =========================
# Asosiy menyuga qaytish
# =========================

from keyboards.reply import start_menu_kb, main_menu_registered

@router.message(F.text == "🏠 Bosh menu")
async def go_home(message: Message, state: FSMContext):
    await state.clear()

    async with SessionLocal() as session:
        result = await session.execute(
            select(User.is_registered).where(
                User.telegram_id == message.from_user.id
            )
        )
        is_registered = result.scalar()

    if is_registered:
        await message.answer(
            "🏠 Asosiy menyu",
            reply_markup=main_menu_registered()
        )
    else:
        await message.answer(
            "🏠 Asosiy menyu",
            reply_markup=start_menu_kb()
        )


# =========================
# Biz haqimizda
# =========================

@router.message(F.text == "ℹ️ Biz haqimizda")
async def about_us(message: Message):
    await message.answer(
        "🏢 Smartlife kompaniyasi\n\n"
        "Smartlife — ishonchli texnika va qulay xizmatlar taqdim etuvchi kompaniya.\n"
        "Biz mijozlarga sifatli mahsulotlar va qulay shartlar bilan xizmat ko‘rsatamiz.\n\n"
        "📍 Hududingizdagi Smartlife kanallariga qo‘shiling va yangiliklardan xabardor bo‘ling.",
        reply_markup=back_kb()
    )
