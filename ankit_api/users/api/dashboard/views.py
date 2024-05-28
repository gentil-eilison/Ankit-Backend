from datetime import datetime

import pytz
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from ankit_api.study_sessions import serializers
from ankit_api.study_sessions.api.filtersets import LanguageHistoricFilter
from ankit_api.study_sessions.models import Language

User = get_user_model()


class StudySessionCountByLanguageView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.StudySessionsByLanguageSerializer
    filterset_class = LanguageHistoricFilter

    def get_queryset(self):
        history_before = self.request.query_params.get("history_date_before", None)
        history_after = self.request.query_params.get("history_date_after", None)
        if history_before or history_after:
            return Language.history.all().order_by("id")
        return (
            Language.history.filter(
                history_date__date__lte=datetime.now(
                    tz=pytz.timezone(settings.TIME_ZONE),
                ),
            )
            .latest_of_each()
            .order_by("id")
        )


class AddedCardsByLanguageView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CardsAddedByLanguageSerializer
    filterset_class = LanguageHistoricFilter

    def get_queryset(self):
        history_before = self.request.query_params.get("history_date_before", None)
        history_after = self.request.query_params.get("history_date_after", None)
        if history_before or history_after:
            return Language.history.all().order_by("id")
        return (
            Language.history.filter(
                history_date__date__lte=datetime.now(
                    tz=pytz.timezone(settings.TIME_ZONE),
                ),
            )
            .latest_of_each()
            .order_by("id")
        )
