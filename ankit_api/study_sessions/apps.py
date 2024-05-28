from django.apps import AppConfig


class StudySessionsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ankit_api.study_sessions"

    def ready(self):
        from . import signals  # noqa: F401

        return super().ready()
