from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from sqlalchemy import select, func, and_

from database import SessionLocal
from models import User

UZ_TZ = ZoneInfo("Asia/Tashkent")


async def get_full_statistics():
    now = datetime.now(UZ_TZ)

    # Bugun
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)

    # Oxirgi 7 kun
    week_start = today_start - timedelta(days=6)

    # Joriy oy
    month_start = today_start.replace(day=1)

    async with SessionLocal() as session:
        # ===== JAMI =====
        total_registered = (await session.execute(
            select(func.count(User.id))
            .where(User.is_registered == True)
        )).scalar()

        total_left = (await session.execute(
            select(func.count(User.id))
            .where(User.left_at.is_not(None))
        )).scalar()

        # ===== BUGUN =====
        today_joined = (await session.execute(
            select(func.count(User.id)).where(
                and_(
                    User.joined_at >= today_start,
                    User.joined_at < today_end
                )
            )
        )).scalar()

        today_left = (await session.execute(
            select(func.count(User.id)).where(
                and_(
                    User.left_at >= today_start,
                    User.left_at < today_end
                )
            )
        )).scalar()

        # ===== OXIRGI 7 KUN =====
        week_joined = (await session.execute(
            select(func.count(User.id)).where(
                and_(
                    User.joined_at >= week_start,
                    User.joined_at < today_end
                )
            )
        )).scalar()

        week_left = (await session.execute(
            select(func.count(User.id)).where(
                and_(
                    User.left_at >= week_start,
                    User.left_at < today_end
                )
            )
        )).scalar()

        # ===== JORIY OY =====
        month_joined = (await session.execute(
            select(func.count(User.id)).where(
                and_(
                    User.joined_at >= month_start,
                    User.joined_at < today_end
                )
            )
        )).scalar()

        month_left = (await session.execute(
            select(func.count(User.id)).where(
                and_(
                    User.left_at >= month_start,
                    User.left_at < today_end
                )
            )
        )).scalar()

    return {
        "total_registered": total_registered,
        "total_left": total_left,

        "today_joined": today_joined,
        "today_left": today_left,

        "week_joined": week_joined,
        "week_left": week_left,

        "month_joined": month_joined,
        "month_left": month_left,
    }
