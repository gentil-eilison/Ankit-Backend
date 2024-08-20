from django.contrib import admin
from rangefilter.filters import DateRangeFilter


class ModelLogAdmin(admin.ModelAdmin):
    def get_list_filter(self, request):
        list_filter = super().get_list_filter(request)
        list_filter += ("history_date", DateRangeFilter)
        return [list_filter]
