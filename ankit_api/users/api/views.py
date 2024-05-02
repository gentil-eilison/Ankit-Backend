import environ
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework import mixins
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ankit_api.users.models import Student
from ankit_api.users.models import User

from . import serializers


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()
    lookup_field = "pk"

    @action(detail=False)
    def me(self, request):
        serializer = serializers.UserSerializer(
            request.user,
            context={"request": request},
        )
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class StudentCreateListView(ListCreateAPIView):
    queryset = Student.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return serializers.StudentReadSerializer
        return serializers.StudentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = environ.Env().str("GOOGLE_APP_CALLBACK_URL")
    client_class = OAuth2Client
