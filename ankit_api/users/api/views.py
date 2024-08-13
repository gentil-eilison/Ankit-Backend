import environ
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.registration.views import SocialConnectView
from dj_rest_auth.registration.views import SocialLoginView
from django.db import IntegrityError
from django.db.models.query import QuerySet
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ankit_api.users.models import Nationality
from ankit_api.users.models import Student
from ankit_api.users.models import User

from . import serializers


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.none()
    lookup_field = "pk"

    def get_queryset(self) -> QuerySet:
        return User.objects.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = serializers.UserSerializer(
            request.user,
            context={"request": request},
        )
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class AnkitSignUpView(RegisterView):
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response(
                {"data": "Já existe um usuário com esse e-mail"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class StudentCreateListView(ListCreateAPIView):
    queryset = Student.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return serializers.StudentReadSerializer
        return serializers.StudentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class StudentUpdateView(UpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = serializers.StudentSerializer
    permission_classes = (permissions.IsAuthenticated,)


class RemoveStudentProfilePictureView(UpdateAPIView):
    queryset = Student.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        student = self.get_object()
        student.profile_picture = ""
        student.save()
        return Response(data={}, status=status.HTTP_200_OK)


class CustomGoogleOAuth2Adapter(GoogleOAuth2Adapter):
    def complete_login(self, request, app, token, response, **kwargs):
        data = None
        id_token = None
        if id_token:
            data = self._decode_id_token(app, id_token)
            if self.fetch_userinfo and "picture" not in data:
                info = self._fetch_user_info(token.token)
                picture = info.get("picture")
                if picture:
                    data["picture"] = picture
        else:
            data = self._fetch_user_info(token.token)
        return self.get_provider().sociallogin_from_response(request, data)


class GoogleLogin(SocialLoginView):
    adapter_class = CustomGoogleOAuth2Adapter
    callback_url = environ.Env().str("GOOGLE_APP_CALLBACK_URL")
    client_class = OAuth2Client


class GoogleConnect(SocialConnectView):
    adapter_class = CustomGoogleOAuth2Adapter
    callback_url = environ.Env().str("GOOGLE_APP_CALLBACK_URL")
    client_class = OAuth2Client


class NationalityListView(ListAPIView):
    queryset = Nationality.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.NationalitySerializer
