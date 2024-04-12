from datetime import timedelta
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history import models as simple_history_models

from ankit_api.core.models import TimeStampedModel
from ankit_api.study_sessions.classes.anki_card import AnkiCard
from ankit_api.study_sessions.classes.csv_maker import FlashCardsCSVMaker
from ankit_api.users.utils import user_directory_path


class Language(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    icon = models.FileField(verbose_name=_("Icon"), blank=True)
    history = simple_history_models.HistoricalRecords()

    class Meta:
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")

    def __str__(self):
        return f"{self.name}"


class StudySession(TimeStampedModel):
    duration_in_minutes = models.DurationField(
        verbose_name=_("Duration in minutes"),
        blank=True,
        default=timedelta(minutes=0),
    )
    cards_added = models.PositiveSmallIntegerField(
        verbose_name=_("Cards added"),
        blank=True,
        default=0,
    )
    csv_file = models.FileField(
        upload_to=user_directory_path,
        verbose_name=_("Spreadsheet file"),
        blank=True,
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

    def add_flaschards_file(self, cards_data) -> None:
        csv_maker = FlashCardsCSVMaker(
            [AnkiCard(front=card["front"], back=card["back"]) for card in cards_data],
        )
        csv_maker.generate_csv()
        path = Path(csv_maker.filename)
        with path.open("rb") as file:
            self.csv_file = File(file, path.name)
            self.save()
        csv_maker.clean()
