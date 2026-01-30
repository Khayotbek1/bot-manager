from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.inline import CHANNELS_BY_REGION


# =================================================
# START / USER MENUS
# =================================================

def start_menu_kb():
    """
    /start dan keyingi asosiy menyu
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📝 Ro'yxatdan o'tish"),
                KeyboardButton(text="ℹ️ Biz haqimizda"),
            ]
        ],
        resize_keyboard=True
    )


def register_kb():
    """
    Faqat ro'yxatdan o'tish (eski joylar uchun qoldirildi)
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Ro'yxatdan o'tish")],
        ],
        resize_keyboard=True
    )


def back_kb():
    """
    Asosiy menyuga qaytish (Biz haqimizda va umumiy joylar)
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⬅️ Ortga")],
        ],
        resize_keyboard=True
    )


def back_step_kb():
    """
    Registration jarayonida 1 qadam orqaga qaytish
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⬅️ Ortga")],
        ],
        resize_keyboard=True
    )


def phone_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="📞 Telefon raqam jo'natish",
                    request_contact=True
                )
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🏠 Bosh menu")]
        ],
        resize_keyboard=True
    )


# =================================================
# ADMIN MAIN PANEL
# =================================================

def admin_main_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📊 Statistika"),
                KeyboardButton(text="📤 Export"),
            ],
            [
                KeyboardButton(text="📝 Post"),
                KeyboardButton(text="🏠 Bosh menu"),
            ],
        ],
        resize_keyboard=True
    )


# =================================================
# ADMIN EXPORT
# =================================================

def export_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📅 Bugun"),
                KeyboardButton(text="🗂 Filter"),
            ],
            [
                KeyboardButton(text="⬅️ Ortga"),
            ],
        ],
        resize_keyboard=True
    )


# =================================================
# ADMIN STATISTICS
# =================================================

def admin_stats_menu_kb():
    """
    📊 Statistika → asosiy menyu (2x2 grid)
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="👥 Jami"),
                KeyboardButton(text="📅 Bugun"),
            ],
            [
                KeyboardButton(text="🗓 Oxirgi 7 kun"),
                KeyboardButton(text="📉 Joriy oy"),
            ],
            [
                KeyboardButton(text="📢 Kanallar bo‘yicha"),
            ],
            [
                KeyboardButton(text="⬅️ Ortga"),
            ],
        ],
        resize_keyboard=True
    )


def admin_channels_kb():
    """
    📢 Kanallar bo‘yicha → kanallar ro‘yxati (2 ustunli)
    """
    buttons = []
    row = []

    for region_channels in CHANNELS_BY_REGION.values():
        for ch in region_channels.values():
            row.append(KeyboardButton(text=ch["title"]))

            if len(row) == 2:
                buttons.append(row)
                row = []

    if row:
        buttons.append(row)

    buttons.append([KeyboardButton(text="⬅️ Ortga")])

    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )


def admin_channel_stats_kb():
    """
    Bitta kanal ichidagi statistika (2x2 grid)
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="👥 Jami"),
                KeyboardButton(text="📅 Bugun"),
            ],
            [
                KeyboardButton(text="🗓 Oxirgi 7 kun"),
                KeyboardButton(text="📉 Joriy oy"),
            ],
            [
                KeyboardButton(text="⬅️ Ortga"),
            ],
        ],
        resize_keyboard=True
    )

def main_menu_registered():
    """
    Ro‘yxatdan O‘TGAN userlar uchun asosiy menyu
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="ℹ️ Biz haqimizda"),
            ]
        ],
        resize_keyboard=True
    )

