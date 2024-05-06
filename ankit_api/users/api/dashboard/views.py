from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from ankit_api.study_sessions.models import Language
from ankit_api.study_sessions.serializers import StudySessionsByLanguageSerializer

User = get_user_model()


class StudySessionCountByLanguageView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Language.objects.all()
    serializer_class = StudySessionsByLanguageSerializer

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(study_sessions__user=self.request.user)
            .distinct()
        )
