from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

regions = [
    "Andijon viloyati", "Buxoro viloyati", "Fargʻona viloyati",
    "Jizzax viloyati", "Xorazm viloyati", "Namangan viloyati",
    "Navoiy viloyati", "Qashqadaryo viloyati",
    "Qoraqalpogʻiston Respublikasi", "Samarqand viloyati",
    "Sirdaryo viloyati", "Surxondaryo viloyati",
    "Toshkent va Toshkent viloyati"
]

def regions_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=r, callback_data=r)]
            for r in regions
        ]
    )

def join_channel_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 Kanalga kirish",
                    url="https://t.me/+JvL4ZWQ1iEdkOTJi"
                )
            ]
        ]
    )
