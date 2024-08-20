from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from ankit_api.core.admin import ModelLogAdmin

from .models import Language
from .models import StudySession


@admin.register(StudySession)
class StudySessionHistoryAdmin(SimpleHistoryAdmin):
    search_fields = ["name"]
    history_list_display = ["history_type"]


@admin.register(StudySession.history.model)
class StudySessionLogAdmin(ModelLogAdmin):
    search_fields = ["name"]
    list_filter = [
        ("language", admin.RelatedOnlyFieldListFilter),
    ]


@admin.register(Language)
class LanguageHistoryAdmin(SimpleHistoryAdmin):
    search_fields = ["name"]
    history_list_display = ["history_type"]


@admin.register(Language.history.model)
class LanguageLogAdmin(ModelLogAdmin):
    search_fields = ["name"]
