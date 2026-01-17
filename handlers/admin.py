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

from states import AdminPostState, AdminSection


router = Router()


# ================= ADMIN CHECK =================

def is_admin(user_id: int) -> bool:
    return user_id in ADMINS


# ================= ADMIN PANEL =================

@router.message(F.text == "/admin")
async def admin_panel(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Kechirasiz, sizga admin huquqi berilmagan!")
        return

    await state.clear()
    await message.answer(
        "👨‍💼 <b>Admin panel</b>",
        reply_markup=admin_main_kb()
    )


# ================= NAVIGATION =================

@router.message(F.text == "⬅️ Ortga")
@router.message(F.text == "🏠 Bosh menu")
async def back_or_exit(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    await state.clear()

    if message.text == "🏠 Bosh menu":
        await message.answer(
            "Assalomu alaykum!\nRo'yxatdan o'tish uchun pastdagi tugmani bosing.",
            reply_markup=register_kb()
        )
    else:
        await message.answer(
            "👨‍💼 Admin panel",
            reply_markup=admin_main_kb()
        )


# ================= EXPORT =================

@router.message(F.text == "📤 Export")
async def export_menu(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    await state.set_state(AdminSection.export)
    await message.answer(
        "📤 <b>Export bo‘limi</b>",
        reply_markup=export_kb()
    )


@router.message(AdminSection.export, F.text == "📅 Bugun")
async def export_today_handler(message: Message):
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


@router.message(AdminSection.export, F.text == "🗂 Filter")
async def export_filter(message: Message):
    await message.answer(
        "📆 Sanalarni kiriting.\n"
        "Namuna: 01.12.2025 31.12.2025",
        reply_markup=export_kb()
    )


@router.message(AdminSection.export, F.text.regexp(r"^\d{2}\.\d{2}\.\d{4}\s\d{2}\.\d{2}\.\d{4}$"))
async def export_range_handler(message: Message):
    path = await export_range_by_text(message.text)
    if not path:
        await message.answer("❗ Ma’lumot topilmadi.", reply_markup=export_kb())
        return

    await message.answer_document(FSInputFile(path))
    os.remove(path)

    await message.answer("⬅️ Ortga qaytishingiz mumkin", reply_markup=export_kb())


# ================= STATISTICS =================

@router.message(F.text == "📊 Statistika")
async def statistics_menu(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    await state.set_state(AdminSection.statistics)
    await message.answer(
        "📊 Statistikani tanlang:",
        reply_markup=admin_stats_menu_kb()
    )


@router.message(AdminSection.statistics, F.text.in_(["👥 Jami", "📅 Bugun", "🗓 Oxirgi 7 kun", "📉 Joriy oy"]))
async def global_stats(message: Message):
    stats = await get_full_statistics()

    mapping = {
        "👥 Jami": (
            "👥 Jami statistika",
            stats["total_registered"],
            stats["total_left"]
        ),
        "📅 Bugun": (
            "📅 Bugungi statistika",
            stats["today_joined"],
            stats["today_left"]
        ),
        "🗓 Oxirgi 7 kun": (
            "🗓 Oxirgi 7 kun",
            stats["week_joined"],
            stats["week_left"]
        ),
        "📉 Joriy oy": (
            "📉 Joriy oy",
            stats["month_joined"],
            stats["month_left"]
        ),
    }

    title, joined, left = mapping[message.text]

    await message.answer(
        f"{title}\n\n➕ Qo‘shilganlar: {joined}\n➖ Chiqib ketganlar: {left}",
        reply_markup=admin_stats_menu_kb()
    )


@router.message(AdminSection.statistics, F.text == "📢 Kanallar bo‘yicha")
async def channels_menu(message: Message, state: FSMContext):
    await state.set_state(AdminSection.channel_statistics)
    await message.answer(
        "📢 Kanalni tanlang:",
        reply_markup=admin_channels_kb()
    )


@router.message(AdminSection.channel_statistics, lambda m: m.text.startswith("📢 "))
async def choose_channel(message: Message, state: FSMContext):
    title = message.text.replace("📢", "").strip()
    channel_key = None

    for region_channels in CHANNELS_BY_REGION.values():
        for key, ch in region_channels.items():
            if ch["title"].endswith(title):
                channel_key = key
                break

    if not channel_key:
        return

    await state.update_data(channel_key=channel_key)

    await message.answer(
        f"{message.text} statistikasi:",
        reply_markup=admin_channel_stats_kb()
    )


@router.message(AdminSection.channel_statistics, F.text.in_(["👥 Jami", "📅 Bugun", "🗓 Oxirgi 7 kun", "📉 Joriy oy"]))
async def channel_stats(message: Message, state: FSMContext):
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


# ================= POST =================

@router.message(F.text == "📝 Post")
async def post_start(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    await state.clear()
    await message.answer(
        "📢 Kontentni yuboring.\n⬅️ Bekor qilish uchun Ortga bosing."
    )
    await state.set_state(AdminPostState.waiting_content)


@router.message(AdminPostState.waiting_content)
async def post_send(message: Message, state: FSMContext):
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
        f"✅ Xabar yuborildi!\n👤 Yuborildi: {sent}\n❌ Yetmadi: {failed}",
        reply_markup=admin_main_kb()
    )

    await state.clear()
