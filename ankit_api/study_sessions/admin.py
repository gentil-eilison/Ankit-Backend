from django.contrib import admin

from .models import Language
from .models import StudySession

admin.site.register(StudySession)
admin.site.register(Language)
