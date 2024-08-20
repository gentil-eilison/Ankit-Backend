# ruff: noqa: DTZ001

import datetime

import pytz
from django.conf import settings

TIME_ZONE = pytz.timezone(settings.TIME_ZONE)


def get_today_midnight() -> datetime.datetime:
    today = datetime.datetime.now(tz=TIME_ZONE)

    # no timezone here because it will result in not being midnight
    return datetime.datetime(
        year=today.year,
        month=today.month,
        day=today.day,
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
