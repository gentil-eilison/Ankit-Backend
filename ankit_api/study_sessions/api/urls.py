from django.urls import path

from . import views

app_name = "study_sessions"

urlpatterns = [
    path(
        "vocabulary_builder/",
        views.VocabularyBuilderView.as_view(),
        name="vocabulary-builder",
    ),
    path("languages/", views.LanguagesListView.as_view(), name="languages-list"),
]
