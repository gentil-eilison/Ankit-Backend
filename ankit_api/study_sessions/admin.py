from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from ankit_api.core.admin import ModelLogAdmin

from .models import Language
from .models import StudySession


@admin.register(StudySession)
class StudySessionHistoryAdmin(SimpleHistoryAdmin):
    search_fields = ["name"]


class StudySessionLogAdmin(ModelLogAdmin):
    search_fields = ["name"]
    list_filter = [
        ("language", admin.RelatedOnlyFieldListFilter),
    ]


@admin.register(Language)
class LanguageHistoryAdmin(SimpleHistoryAdmin):
    search_fields = ["name"]


class LanguageLogAdmin(ModelLogAdmin):
    search_fields = ["name"]


admin.site.register(StudySession.history.model, StudySessionLogAdmin)

admin.site.register(Language.history.model, LanguageLogAdmin)
