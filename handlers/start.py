from aiogram import Router
from aiogram import F
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards.reply import register_kb

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Assalomu alaykum!\n"
        "Ro'yxatdan o'tish uchun pastdagi tugmani bosing.",
        reply_markup=register_kb()
    )



@router.message(F.text == "🏠 Bosh menu")
async def user_back_to_main(message: Message):
    await message.answer(
        "Assalomu alaykum!\nRo'yxatdan o'tish uchun pastdagi tugmani bosing.",
        reply_markup=register_kb()
    )
