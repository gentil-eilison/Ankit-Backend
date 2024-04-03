# Create your views here.
from .models import StudySession
from rest_framework import permissions, viewsets

from .serializers import StudySessionSerializer


class StudySessionViewSet(viewsets.ModelViewSet):
    queryset = StudySession.objects.all()
    serializer_class = StudySessionSerializer
    permission_classes = (permissions.IsAuthenticated,)
