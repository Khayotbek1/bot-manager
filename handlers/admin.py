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

from keyboards.reply import (
    admin_main_kb,
    export_kb,
    register_kb,
    admin_stats_menu_kb,
    admin_channels_kb,
    admin_channel_stats_kb,
)

from keyboards.inline import CHANNELS_BY_REGION

from utils.csv_export import export_today, export_range_by_text
from utils.statistics import (
    get_full_statistics,
    get_channel_period_stats,
)

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
async def admin_exit_to_user_menu(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    await state.clear()
    await message.answer(
        "Assalomu alaykum!\nRo'yxatdan o'tish uchun pastdagi tugmani bosing.",
        reply_markup=register_kb()
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
            "❗ Bu sana oralig‘ida ma’lumot topilmadi yoki format noto‘g‘ri.",
            reply_markup=export_kb()
        )
        return

    await message.answer_document(FSInputFile(path))
    os.remove(path)

    await message.answer(
        "⬅️ Ortga qaytishingiz mumkin",
        reply_markup=export_kb()
    )


# ================= STATISTICS (REPLY KEYBOARD) =================

@router.message(F.text == "📊 Statistika")
async def statistics_menu(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    await state.clear()
    await message.answer(
        "📊 Statistikani tanlang:",
        reply_markup=admin_stats_menu_kb()
    )


@router.message(F.text.in_(["👥 Jami", "📅 Bugun", "🗓 Oxirgi 7 kun", "📉 Joriy oy"]))
async def global_stats(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    data = await state.get_data()
    if "channel_key" in data:
        return

    stats = await get_full_statistics()

    if message.text == "👥 Jami":
        text = (
            "👥 Jami statistika\n\n"
            f"➕ Ro‘yxatdan o‘tganlar: {stats['total_registered']}\n"
            f"➖ Chiqib ketganlar: {stats['total_left']}"
        )
    elif message.text == "📅 Bugun":
        text = (
            "📅 Bugungi statistika\n\n"
            f"➕ Qo‘shilganlar: {stats['today_joined']}\n"
            f"➖ Chiqib ketganlar: {stats['today_left']}"
        )
    elif message.text == "🗓 Oxirgi 7 kun":
        text = (
            "🗓 Oxirgi 7 kun\n\n"
            f"➕ Qo‘shilganlar: {stats['week_joined']}\n"
            f"➖ Chiqib ketganlar: {stats['week_left']}"
        )
    else:
        text = (
            "📉 Joriy oy\n\n"
            f"➕ Qo‘shilganlar: {stats['month_joined']}\n"
            f"➖ Chiqib ketganlar: {stats['month_left']}"
        )

    await message.answer(text, reply_markup=admin_stats_menu_kb())


@router.message(F.text == "📢 Kanallar bo‘yicha")
async def channels_menu(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    await state.clear()
    await message.answer(
        "📢 Kanalni tanlang:",
        reply_markup=admin_channels_kb()
    )


@router.message(lambda m: m.text.startswith("📢 "))
async def choose_channel(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    title = message.text.replace("📢", "").strip()
    channel_key = None

    for region_channels in CHANNELS_BY_REGION.values():
        for key, ch in region_channels.items():
            if ch["title"].endswith(title):
                channel_key = key
                break

    if not channel_key:
        return

    await state.clear()
    await state.update_data(channel_key=channel_key)

    await message.answer(
        f"📢 {message.text} statistikasi:",
        reply_markup=admin_channel_stats_kb()
    )


@router.message(F.text.in_(["👥 Jami", "📅 Bugun", "🗓 Oxirgi 7 kun", "📉 Joriy oy"]))
async def channel_stats(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    data = await state.get_data()
    channel_key = data.get("channel_key")
    if not channel_key:
        return

    period_map = {
        "👥 Jami": "total",
        "📅 Bugun": "today",
        "🗓 Oxirgi 7 kun": "week",
        "📉 Joriy oy": "month",
    }

    stats = await get_channel_period_stats(channel_key, period_map[message.text])

    await message.answer(
        f"{message.text} — kanal bo‘yicha\n\n"
        f"➕ Qo‘shilganlar: {stats['joined']}\n"
        f"➖ Chiqib ketganlar: {stats['left']}",
        reply_markup=admin_channel_stats_kb()
    )


# ================= POST (BROADCAST) =================

@router.message(F.text == "📝 Post")
async def post_start(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    await message.answer(
        "📢 Botdan ro‘yxatdan o‘tgan barcha foydalanuvchilarga yuboriladigan "
        "kontentni jo‘nating.\n\n"
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

    sent, failed = 0, 0

    for user_id in users:
        try:
            await message.copy_to(chat_id=user_id)
            sent += 1
            await asyncio.sleep(0.05)
        except (TelegramForbiddenError, TelegramBadRequest):
            failed += 1

    await message.answer(
        "✅ Xabar yuborildi!\n\n"
        f"👤 Yuborildi: {sent}\n"
        f"❌ Yetib bormadi: {failed}",
        reply_markup=admin_main_kb()
    )

    await state.clear()
