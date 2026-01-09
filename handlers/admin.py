import os
import asyncio

from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest

from sqlalchemy import select

from config import ADMINS
from database import SessionLocal
from models import User
from keyboards.reply import admin_main_kb, export_kb
from utils.csv_export import export_today, export_range_by_text
from utils.statistics import get_full_statistics
from states import AdminPostState


router = Router()


# ================= ADMIN CHECK =================

def is_admin(user_id: int) -> bool:
    return user_id in ADMINS


# ================= ADMIN PANEL =================

@router.message(F.text == "/admin")
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Kechirasiz, sizga admin huquqi berilmagan!")
        return

    await message.answer(
        "👨‍💼 <b>Admin panel</b>",
        reply_markup=admin_main_kb()
    )


# ================= NAVIGATION =================

@router.message(F.text == "⬅️ Ortga")
async def back_to_admin_menu(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    await state.clear()
    await message.answer(
        "👨‍💼 Admin panel",
        reply_markup=admin_main_kb()
    )


@router.message(F.text == "🏠 Bosh menu")
async def back_to_main_menu(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    await state.clear()
    await message.answer(
        "🏠 Bosh menu",
        reply_markup=admin_main_kb()
    )


# ================= EXPORT =================

@router.message(F.text == "📤 Export")
async def export_menu(message: Message):
    if not is_admin(message.from_user.id):
        return

    await message.answer(
        "📤 <b>Export bo‘limi</b>",
        reply_markup=export_kb()
    )


@router.message(F.text == "📅 Bugun")
async def export_today_handler(message: Message):
    if not is_admin(message.from_user.id):
        return

    path = await export_today()

    if not path:
        await message.answer("❗ Bugun uchun ma’lumot topilmadi.")
        return

    await message.answer_document(FSInputFile(path))
    os.remove(path)

    await message.answer(
        "⬅️ Ortga qaytishingiz mumkin",
        reply_markup=export_kb()
    )


@router.message(F.text == "🗂 Filter")
async def export_filter(message: Message):
    if not is_admin(message.from_user.id):
        return

    await message.answer(
        "📆 Sanalarni kiriting.\n"
        "Namuna: 01.12.2025 31.12.2025\n\n"
        "⬅️ Ortga tugmasi bilan qaytishingiz mumkin",
        reply_markup=export_kb()
    )


@router.message(F.text.regexp(r"^\d{2}\.\d{2}\.\d{4}\s\d{2}\.\d{2}\.\d{4}$"))
async def export_range_handler(message: Message):
    if not is_admin(message.from_user.id):
        return

    path = await export_range_by_text(message.text)

    if not path:
        await message.answer(
            "❗ Bu sana oralig‘ida ma’lumot topilmadi yoki format noto‘g‘ri.\n"
            "Namuna: 01.12.2025 31.12.2025",
            reply_markup=export_kb()
        )
        return

    await message.answer_document(FSInputFile(path))
    os.remove(path)

    await message.answer(
        "⬅️ Ortga qaytishingiz mumkin",
        reply_markup=export_kb()
    )


# ================= STATISTICS =================

@router.message(F.text == "📊 Statistika")
async def statistics(message: Message):
    if not is_admin(message.from_user.id):
        return

    stats = await get_full_statistics()

    await message.answer(
        "📊 <b>Kanal statistikasi</b>\n\n"

        "👥 <b>Jami</b>\n"
        f"➕ Ro‘yxatdan o‘tganlar: <b>{stats['total_registered']}</b>\n"
        f"➖ Chiqib ketganlar: <b>{stats['total_left']}</b>\n\n"

        "📅 <b>Bugun</b>\n"
        f"➕ Qo‘shilganlar: <b>{stats['today_joined']}</b>\n"
        f"➖ Chiqib ketganlar: <b>{stats['today_left']}</b>\n\n"

        "🗓 <b>Oxirgi 7 kun</b>\n"
        f"➕ Qo‘shilganlar: <b>{stats['week_joined']}</b>\n"
        f"➖ Chiqib ketganlar: <b>{stats['week_left']}</b>\n\n"

        "📉 <b>Joriy oy</b>\n"
        f"➕ Qo‘shilganlar: <b>{stats['month_joined']}</b>\n"
        f"➖ Chiqib ketganlar: <b>{stats['month_left']}</b>",
        reply_markup=admin_main_kb()
    )


# ================= POST (BROADCAST) =================

@router.message(F.text == "📝 Post")
async def post_start(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    await message.answer(
        "📢 Botdan ro‘yxatdan o‘tgan barcha foydalanuvchilarga yuboriladigan "
        "kontentni jo‘nating.\n\n"
        "Text, rasm, video yoki fayl bo‘lishi mumkin.\n"
        "⬅️ Bekor qilish uchun Ortga tugmasini bosing."
    )
    await state.set_state(AdminPostState.waiting_content)


@router.message(AdminPostState.waiting_content)
async def post_send(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    async with SessionLocal() as session:
        users = (await session.execute(
            select(User.telegram_id).where(User.is_registered == True)
        )).scalars().all()

    sent = 0
    failed = 0

    for user_id in users:
        try:
            await message.copy_to(chat_id=user_id)
            sent += 1
            await asyncio.sleep(0.05)
        except (TelegramForbiddenError, TelegramBadRequest):
            failed += 1
        except Exception:
            failed += 1

    await message.answer(
        "✅ Xabar yuborildi!\n\n"
        f"👤 Yuborildi: <b>{sent}</b>\n"
        f"❌ Yetib bormadi: <b>{failed}</b>",
        reply_markup=admin_main_kb()
    )

    await state.clear()
