from dj_rest_auth.registration import views as dj_rest_auth_views
from django.urls import include
from django.urls import path

from . import views as users_views
from .dashboard import views as dashboard_views

app_name = "users"

urlpatterns = [
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
        dj_rest_auth_views.SocialAccountDisconnectView.as_view(),
        name="social-account-disconnect",
    ),
    path(
        "dj_rest_auth/socialaccounts/",
        dj_rest_auth_views.SocialAccountListView.as_view(),
        name="social-accounts-list-view",
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
        "students/<int:pk>/remove_profile_pic/",
        users_views.RemoveStudentProfilePictureView.as_view(),
        name="remove-students-profile-picture",
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
