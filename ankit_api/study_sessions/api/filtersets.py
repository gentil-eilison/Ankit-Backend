from django_filters import rest_framework as filters

from ankit_api.study_sessions.models import Language
from ankit_api.study_sessions.models import StudySession


class StudySessionHistoricFilter(filters.FilterSet):
    date = filters.DateRangeFilter(field_name="created_at")

    class Meta:
        model = Language
        fields = ("date",)


class StudySessionFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = StudySession
        fields = ("language",)
