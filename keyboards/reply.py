from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# ================= USER KEYBOARDS =================

def register_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Ro'yxatdan o'tish")]
        ],
        resize_keyboard=True
    )


def phone_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📞 Telefon raqam jo'natish", request_contact=True)]
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


# ================= ADMIN KEYBOARDS =================

def admin_main_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Statistika")],
            [KeyboardButton(text="📤 Export")],
            [KeyboardButton(text="📝 Post")],
            [KeyboardButton(text="🏠 Bosh menu")]
        ],
        resize_keyboard=True
    )


def export_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📅 Bugun")],
            [KeyboardButton(text="🗂 Filter")],
            [KeyboardButton(text="⬅️ Ortga")],
        ],
        resize_keyboard=True
    )
