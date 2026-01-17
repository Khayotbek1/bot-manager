from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

CHANNELS_BY_REGION = {
    "Fargʻona viloyati": {
        "smartlife_fargona": {
            "title": "📢 Smartlife Fargʻona",
            "url": "https://t.me/+i5AOxrp9VnoxOGQy",
            "chat_id": -1001247697546
        },
        "smartlife_qoqon": {
            "title": "📢 Smartlife Qo‘qon",
            "url": "PASTE_LINK_HERE",
            "chat_id": -1001234567890

        }
    },
    "Andijon viloyati": {
        "smartlife_andijon": {
            "title": "📢 Smartlife Andijon",
            "url": "PASTE_LINK_HERE",
            "chat_id": -1001234567890
        }
    }
}

regions = [
    "Andijon viloyati", "Buxoro viloyati", "Fargʻona viloyati",
    "Jizzax viloyati", "Xorazm viloyati", "Namangan viloyati",
    "Navoiy viloyati", "Qashqadaryo viloyati",
    "Qoraqalpogʻiston Respublikasi", "Samarqand viloyati",
    "Sirdaryo viloyati", "Surxondaryo viloyati",
    "Toshkent"
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


def channels_by_region_kb(region: str):
    channels = CHANNELS_BY_REGION.get(region, {})

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=ch["title"],
                    callback_data=f"channel:{key}"
                )
            ]
            for key, ch in channels.items()
        ]
    )


def join_channel_kb(channel_key: str):
    for region_channels in CHANNELS_BY_REGION.values():
        if channel_key in region_channels:
            url = region_channels[channel_key]["url"]
            return InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="📢 Kanalga kirish", url=url)]
                ]
            )
    return None
