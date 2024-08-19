import datetime

import pytz
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from rest_framework import status
from rest_framework import views
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ankit_api.study_sessions import serializers
from ankit_api.study_sessions.api.filtersets import StudySessionHistoricFilter
from ankit_api.study_sessions.models import Language

User = get_user_model()


class HistoricalDataByLanguageView(views.APIView):
    serializer_class = None
    queryset = Language.objects.all().order_by("id")
    annotate_name = ""

    def _get_date_range_filter(self):
        date_from = self.request.query_params.get("date_after")
        date_before = self.request.query_params.get("date_before")

        date_range_query_filter = None

        if date_from:
            date_from = datetime.datetime.fromisoformat(date_from)
        if date_before:
            date_before = datetime.datetime.fromisoformat(date_before)
        if date_from and date_before:
            date_range_query_filter = models.Q(
                study_sessions__created_at__range=(date_from, date_before),
            )
        if date_from and not date_before:
            date_range_query_filter = models.Q(
                study_sessions__created_at__gte=date_from,
            )
        if not date_from and date_before:
            date_range_query_filter = models.Q(
                study_sessions__created_at__lte=date_before,
            )
        return date_range_query_filter & models.Q(
            study_sessions__user=self.request.user,
        )

    def _get_annotate_expression(self):
        pass

    def get(self, *args, **kwargs):
        annotate_expression = self._get_annotate_expression()
        annotate_expression.filter = self._get_date_range_filter()
        annotate = {self.annotate_name: annotate_expression}
        languages = self.queryset.annotate(**annotate)
        languages_serializer = self.serializer_class(instance=languages, many=True)
        return Response(data=languages_serializer.data, status=status.HTTP_200_OK)


class StudySessionCountByLanguageView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.StudySessionsByLanguageSerializer
    filterset_class = StudySessionHistoricFilter

    def get_queryset(self):
        history_before = self.request.query_params.get("history_date_before", None)
        history_after = self.request.query_params.get("history_date_after", None)
        if history_before or history_after:
            return Language.history.all().order_by("id")
        return (
            Language.history.filter(
                history_date__date__lte=datetime.datetime.now(
                    tz=pytz.timezone(settings.TIME_ZONE),
                ),
            )
            .latest_of_each()
            .order_by("id")
        )


class AddedCardsByLanguageView(HistoricalDataByLanguageView):
    permission_classes = (IsAuthenticated,)
    annotate_name = "cards_added"
    serializer_class = serializers.CardsAddedByLanguageSerializer

    def _get_annotate_expression(self):
        return models.Sum(
            "study_sessions__cards_added",
        )
