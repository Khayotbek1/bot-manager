import csv
from datetime import datetime, timedelta, time
from pathlib import Path
from zoneinfo import ZoneInfo
from sqlalchemy import select, and_

from database import SessionLocal
from models import User

UZ_TZ = ZoneInfo("Asia/Tashkent")
DATE_FORMAT = "%d.%m.%Y"


def format_dt(dt):
    if not dt:
        return ""
    return dt.astimezone(UZ_TZ).strftime("%d.%m.%Y %H:%M")


def parse_date_range(text: str):
    """
    Kutilgan format:
    01.01.2026 10.01.2026
    """
    try:
        start_str, end_str = text.strip().split()

        start_date = datetime.strptime(start_str, DATE_FORMAT)
        end_date = datetime.strptime(end_str, DATE_FORMAT)

        # timezone qo‘shamiz
        start_date = start_date.replace(tzinfo=UZ_TZ)
        end_date = datetime.combine(
            end_date.date(),
            time(23, 59, 59),
            tzinfo=UZ_TZ
        )

        return start_date, end_date
    except Exception:
        return None, None


async def write_csv(filename: str, users: list[User]):
    path = Path(filename)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "telegram_id",
            "username",
            "first_name",
            "phone",
            "joined_at",
            "left_at"
        ])

        for u in users:
            writer.writerow([
                u.telegram_id,
                u.username,
                u.first_name,
                u.phone,
                format_dt(u.joined_at),
                format_dt(u.left_at)
            ])

    return path


async def export_today():
    now = datetime.now(UZ_TZ)
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)

    filename = f"users_today_{now.strftime('%d-%m-%Y')}.csv"

    async with SessionLocal() as session:
        users = (await session.execute(
            select(User).where(
                and_(
                    User.joined_at >= start,
                    User.joined_at < end
                )
            )
        )).scalars().all()

    return await write_csv(filename, users)


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
                    User.joined_at >= start_dt,
                    User.joined_at <= end_dt
                )
            )
        )).scalars().all()

    if not users:
        return None

    return await write_csv(filename, users)
