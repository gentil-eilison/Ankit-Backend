from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history import models as simple_history_models

from ankit_api.core.models import TimeStampedModel
from ankit_api.users.utils import user_directory_path


class Language(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    icon = models.FileField(verbose_name=_("Icon"))
    history = simple_history_models.HistoricalRecords()

    class Meta:
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")

    def __str__(self):
        return f"{self.name}"


class StudySession(TimeStampedModel):
    duration_in_minutes = models.DurationField(verbose_name=_("Duration in minutes"))
    cards_added = models.PositiveSmallIntegerField(verbose_name=_("Cards added"))
    spreadsheet_file = models.FileField(
        upload_to=user_directory_path,
        verbose_name=_("Spreadsheet file"),
    )
    language = models.ForeignKey(
        Language,
        related_name="study_sessions",
        on_delete=models.CASCADE,
        verbose_name=_("Language"),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="study_sessions",
        on_delete=models.CASCADE,
        verbose_name=_("User"),
    )
    history = simple_history_models.HistoricalRecords()

    class Meta:
        verbose_name = _("Study Session")
        verbose_name_plural = _("Study Sessions")

    def __str__(self):
        return (
            f"{self.language} session of {self.user.first_name} {self.user.last_name}"
        )
