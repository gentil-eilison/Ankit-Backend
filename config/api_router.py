from django.conf import settings
from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from ankit_api.study_sessions.views import StudySessionViewSet
from ankit_api.study_sessions.views import VocabularyBuilderView
from ankit_api.users.api.views import GoogleLogin
from ankit_api.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register(r"study_sessions", StudySessionViewSet)


app_name = "api"
urlpatterns = router.urls
urlpatterns += [
    path(
        "vocabulary_builder/",
        VocabularyBuilderView.as_view(),
        name="vocabulary-builder",
    ),
    path("dj_rest_auth/", include("dj_rest_auth.urls")),
    path("dj_rest_auth/google/", GoogleLogin.as_view(), name="google-login"),
]
