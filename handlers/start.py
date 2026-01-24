from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.reply import start_menu_kb, back_kb

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

@router.message(F.text == "🏠 Bosh menu")
async def user_back_to_main(message: Message, state: FSMContext):
    await state.clear()
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
