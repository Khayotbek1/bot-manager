from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


CHANNELS_BY_REGION = {
    "Fargʻona viloyati": {
        "smartlife_fargona": {
            "title": "📢 Smartlife Fargʻona",
            "url": "https://t.me/+O7jHYy-QKDhjMzAy",
            "chat_id": -1001247697546
        },
        "smartlife_qoqon": {
            "title": "📢 Smartlife Qo‘qon",
            "url": "https://t.me/+l49Y_Alc9dpkMTdi",
            "chat_id": -1002015239197
        },
        "smartlife_oltiariq": {
            "title": "📢 Smartlife Oltiariq",
            "url": "https://t.me/smartlife_oltiariq",
            "chat_id": -1001640277219
        }
    },
    "Andijon viloyati": {
        "smartlife_andijon": {
            "title": "📢 Smartlife Andijon",
            "url": "https://t.me/+ga96zEENMI40ZDgy",
            "chat_id": -1002262515398
        }
    },
    "Toshkent": {
        "smartlife_toshkent": {
            "title": "📢 Smartlife Toshkent",
            "url": "https://t.me/smartlife_price",
            "chat_id": -1001788954426
        }
    }
}
ALL_CHANNEL_IDS = {
    channel["chat_id"]
    for region in CHANNELS_BY_REGION.values()
    for channel in region.values()
}

REGIONS = [
    "Andijon viloyati", "Buxoro viloyati", "Fargʻona viloyati",
    "Jizzax viloyati", "Xorazm viloyati", "Namangan viloyati",
    "Navoiy viloyati", "Qashqadaryo viloyati",
    "Qoraqalpogʻiston Respublikasi", "Samarqand viloyati",
    "Sirdaryo viloyati", "Surxondaryo viloyati",
    "Toshkent"
]


def regions_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for region in REGIONS:
        kb.button(text=region, callback_data=region)
    kb.adjust(2)
    return kb.as_markup()



def channels_by_region_kb(region: str) -> InlineKeyboardMarkup:

    channels = CHANNELS_BY_REGION.get(region)

    if not channels:
        channels = {}
        for region_channels in CHANNELS_BY_REGION.values():
            channels.update(region_channels)

    kb = InlineKeyboardBuilder()
    for key, ch in channels.items():
        kb.button(
            text=ch["title"],
            callback_data=f"channel:{key}"
        )

    kb.adjust(2)
    return kb.as_markup()


# =================================================
# JOIN CHANNEL (REQUEST LINK)
# =================================================

def join_channel_kb(channel_key: str) -> InlineKeyboardMarkup | None:
    """
    Kanalga so‘rov yuborish uchun LINK
    """
    for region_channels in CHANNELS_BY_REGION.values():
        if channel_key in region_channels:
            url = region_channels[channel_key]["url"]
            return InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="📢 Kanalga so‘rov yuborish",
                            url=url
                        )
                    ]
                ]
            )
    return None


# =================================================
# CHECK JOIN REQUEST
# =================================================

def check_join_kb(channel_key: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Tekshirish",
                    callback_data=f"check_join:{channel_key}"
                )
            ]
        ]
    )

def enter_channel_kb(channel_key: str) -> InlineKeyboardMarkup | None:
    for region_channels in CHANNELS_BY_REGION.values():
        if channel_key in region_channels:
            url = region_channels[channel_key]["url"]
            return InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="📢 Kanalga kirish",
                            url=url
                        )
                    ]
                ]
            )
    return None



# ======================
# CANCEL BUTTON
# ======================

def cancel_post_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="❌ Bekor qilish",
                    callback_data="cancel_post"
                )
            ]
        ]
    )
