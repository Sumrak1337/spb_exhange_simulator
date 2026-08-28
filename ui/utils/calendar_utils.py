import calendar
import datetime
from typing import Any, Dict, List


def generate_year_calendar(year: int) -> List[Dict[str, Any]]:
    days = []
    current = datetime.date(year, 1, 1)
    end = datetime.date(year, 12, 31)

    while current <= end:
        days.append(
            {
                "date": current.isoformat(),
                "day": current.day,
                "month": current.month,
                "year": current.year,
                "weekday": current.weekday(),
                "month_name": current.strftime("%B"),
            }
        )
        current += datetime.timedelta(days=1)

    return days


def get_default_working_days(year: int) -> dict:
    state = {}
    current = datetime.date(year, 1, 1)
    end = datetime.date(year, 12, 31)
    while current <= end:
        state[current.isoformat()] = current.weekday() < 5
        current += datetime.timedelta(days=1)
    return state


def get_month_grid(year: int, month: int) -> list[list]:
    return calendar.monthcalendar(year, month)


def month_key(year: int, month: int) -> str:
    return f"{year}-{month:02d}"
