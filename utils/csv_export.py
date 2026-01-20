import csv
from datetime import datetime, timedelta, time
from pathlib import Path
from zoneinfo import ZoneInfo

from sqlalchemy import select, and_

from database import SessionLocal
from models import User
from keyboards.inline import CHANNELS_BY_REGION


UZ_TZ = ZoneInfo("Asia/Tashkent")
DATE_FORMAT = "%d.%m.%Y"


# ================= TIME HELPERS =================

def to_naive(dt: datetime | None) -> datetime | None:
    """
    TZ-aware datetime -> TZ-naive (Postgres TIMESTAMP WITHOUT TIME ZONE uchun)
    """
    if not dt:
        return None
    return dt.replace(tzinfo=None)


def today_range_naive():
    now = datetime.now(UZ_TZ).replace(tzinfo=None)
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    return start, end, now


# ================= FORMAT HELPERS =================

def format_dt(dt):
    """
    Datetime ni Excel uchun qulay formatga o‘tkazish
    (DB’da tz-naive, ko‘rsatishda Asia/Tashkent)
    """
    if not dt:
        return ""
    return dt.replace(tzinfo=UZ_TZ).strftime("%d.%m.%Y %H:%M")


def parse_date_range(text: str):
    """
    Kutilgan format:
    01.01.2026 10.01.2026
    """
    try:
        start_str, end_str = text.strip().split()

        start_date = datetime.strptime(start_str, DATE_FORMAT)
        end_date = datetime.strptime(end_str, DATE_FORMAT)

        # 👉 DB uchun TZ-NAIVE qilib qaytaramiz
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = datetime.combine(
            end_date.date(),
            time(23, 59, 59)
        )

        return start_date, end_date
    except Exception:
        return None, None


def get_channel_title(channel_key: str) -> str:
    if not channel_key:
        return ""

    for region_channels in CHANNELS_BY_REGION.values():
        if channel_key in region_channels:
            return region_channels[channel_key]["title"]

    return channel_key


# ================= CSV WRITER =================

async def write_csv(filename: str, users: list[User]):
    path = Path(filename)

    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)

        writer.writerow([
            "telegram_id",
            "username",
            "first_name",
            "phone",
            "region",
            "channel",
            "joined_at",
            "left_at",
        ])

        for u in users:
            writer.writerow([
                u.telegram_id,
                u.username,
                u.first_name,
                f"'{u.phone}",          # Excel raqamni buzmasin
                u.region,
                get_channel_title(u.channel),
                format_dt(u.joined_at),
                format_dt(u.left_at),
            ])

    return path


# ================= EXPORT: TODAY =================

async def export_today():
    start, end, now = today_range_naive()

    filename = f"users_today_{now.strftime('%d-%m-%Y')}.csv"

    async with SessionLocal() as session:
        users = (await session.execute(
            select(User).where(
                and_(
                    User.is_registered.is_(True),
                    User.joined_at >= start,
                    User.joined_at < end
                )
            )
        )).scalars().all()

    if not users:
        return None

    return await write_csv(filename, users)


# ================= EXPORT: DATE RANGE =================

async def export_range_by_text(text: str):
    start_dt, end_dt = parse_date_range(text)

    if not start_dt:
        return None

    filename = (
        f"users_{start_dt.strftime('%d-%m-%Y')}_"
        f"to_{end_dt.strftime('%d-%m-%Y')}.csv"
    )

    async with SessionLocal() as session:
        users = (await session.execute(
            select(User).where(
                and_(
                    User.is_registered.is_(True),
                    User.joined_at >= start_dt,
                    User.joined_at <= end_dt
                )
            )
        )).scalars().all()

    if not users:
        return None

    return await write_csv(filename, users)
