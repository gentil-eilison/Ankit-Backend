from django_filters import rest_framework as filters

from ankit_api.study_sessions.models import Language


class LanguageHistoricFilter(filters.FilterSet):
    history_date = filters.DateFromToRangeFilter(
        field_name="history_date__date",
        method="filter_history_date",
    )

    class Meta:
        model = Language.history.model
        fields = ("history_date",)

    def filter_history_date(self, queryset, name, value):
        lookup = {}
        history_after, history_before = value.start, value.stop
        if history_after and history_before:
            lookup[f"{name}__range"] = [history_after, history_before]
        elif history_after and not history_before:
            lookup[f"{name}__gte"] = history_after
        elif not history_after and history_before:
            lookup[f"{name}__lte"] = history_before
        return queryset.filter(**lookup).latest_of_each()
