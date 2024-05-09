from django_filters import rest_framework as filters

from ankit_api.study_sessions.models import Language


class TesteFiltroHistorico(filters.FilterSet):
    history_date = filters.DateFromToRangeFilter(field_name="history_date__date")

    class Meta:
        model = Language.history.model
        fields = ("history_date",)
