from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from ankit_api.study_sessions import serializers
from ankit_api.study_sessions.models import Language

User = get_user_model()


class StudySessionCountByLanguageView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Language.objects.all()
    serializer_class = serializers.StudySessionsByLanguageSerializer

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(study_sessions__user=self.request.user)
            .distinct()
        )


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
