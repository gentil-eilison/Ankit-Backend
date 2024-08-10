from dj_rest_auth.registration.views import SocialAccountDisconnectView
from django.conf import settings
from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from ankit_api.study_sessions.views import StudySessionViewSet
from ankit_api.study_sessions.views import VocabularyBuilderView
from ankit_api.users.api import views as users_views
from ankit_api.users.api.dashboard import views as dashboard_views

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", users_views.UserViewSet)
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
    path(
        "dj_rest_auth/registration/",
        users_views.AnkitSignUpView.as_view(),
        name="dj-rest-auth-registration",
    ),
    path(
        "dj_rest_auth/google/",
        users_views.GoogleLogin.as_view(),
        name="google-login",
    ),
    path(
        "dj_rest_auth/google/connect/",
        users_views.GoogleConnect.as_view(),
        name="google-connect",
    ),
    path(
        "dj_rest_auth/socialaccount/<int:pk>/disconnect/",
        SocialAccountDisconnectView.as_view(),
        name="social-account-disconnect",
    ),
    path(
        "students/",
        users_views.StudentCreateListView.as_view(),
        name="student-create-list",
    ),
    path(
        "students/<int:pk>/",
        users_views.StudentUpdateView.as_view(),
        name="student-update",
    ),
    path(
        "study_sessions_by_language/",
        dashboard_views.StudySessionCountByLanguageView.as_view(),
        name="study-sessions-by-language",
    ),
    path(
        "cards_added_by_language/",
        dashboard_views.AddedCardsByLanguageView.as_view(),
        name="cards-added-by-language",
    ),
    path(
        "nationalities/",
        users_views.NationalityListView.as_view(),
        name="nationality-list",
    ),
]
