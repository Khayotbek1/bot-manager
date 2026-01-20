from datetime import datetime
from zoneinfo import ZoneInfo

UZ_TZ = ZoneInfo("Asia/Tashkent")


def now_naive() -> datetime:
    return datetime.now(UZ_TZ).replace(tzinfo=None)


def day_start_naive(dt: datetime) -> datetime:
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)
