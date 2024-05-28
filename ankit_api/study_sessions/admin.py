from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Language
from .models import StudySession

admin.site.register(StudySession)
admin.site.register(Language, SimpleHistoryAdmin)
