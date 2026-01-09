from aiogram import Router
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
