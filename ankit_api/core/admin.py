import datetime

import pytz
from django.conf import settings
from django.contrib import admin
from rangefilter.filters import DateTimeRangeFilterBuilder

from .utils import get_today_midnight

TIME_ZONE = pytz.timezone(settings.TIME_ZONE)


class ModelLogAdmin(admin.ModelAdmin):
    def get_list_filter(self, request):
        list_filter = super().get_list_filter(request)
        default_start = get_today_midnight()
        history_filter = [
            (
                "history_date",
                DateTimeRangeFilterBuilder(
                    default_end=datetime.datetime.now(tz=TIME_ZONE),
                    default_start=default_start,
                ),
            ),
        ]
        if list_filter:
            history_filter.extend(list_filter)
        return history_filter
