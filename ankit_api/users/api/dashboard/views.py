from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from ankit_api.study_sessions import serializers
from ankit_api.study_sessions.models import Language
from ankit_api.users.api.filtersets import TesteFiltroHistorico
from ankit_api.users.models import Student

User = get_user_model()


class StudySessionCountByLanguageView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.StudySessionsByLanguageSerializer
    filterset_class = TesteFiltroHistorico

    def get_date_for_historical_filter(self):
        lookup = {}
        history_date_before = self.request.query_params.get("history_date_before", None)
        history_date_after = self.request.query_params.get("history_date_after", None)
        if history_date_before and history_date_after:
            lookup["history_date__date__range"] = [
                datetime.fromisoformat(history_date_after),
                datetime.fromisoformat(history_date_before),
            ]
        elif history_date_before and not history_date_after:
            lookup["history_date__date__lte"] = datetime.fromisoformat(
                history_date_before,
            )
        elif not history_date_before and history_date_after:
            lookup["history_date__date__gte"] = datetime.fromisoformat(
                history_date_after,
            )
        else:
            lookup["history_date__date__lte"] = datetime.now(tz=settings.TIME_ZONE)
        return lookup

    def get_queryset(self):
        lookup = self.get_date_for_historical_filter()
        return Language.history.filter(**lookup).latest_of_each().order_by("id")


class AddedCardsByLanguageView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Language.objects.all()
    serializer_class = serializers.CardsAddedByLanguageSerializer

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(study_sessions__user=self.request.user)
            .distinct()
        )


class StudentStudyDataView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Student.objects.filter(user=self.request.user)
