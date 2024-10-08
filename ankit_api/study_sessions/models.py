import csv
from datetime import datetime
from datetime import timedelta
from pathlib import Path

import pytz
from django.conf import settings
from django.core.files import File
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history import models as simple_history_models

from ankit_api.core.models import TimeStampedModel
from ankit_api.study_sessions.classes.anki_card import AnkiCard
from ankit_api.study_sessions.classes.csv_maker import FlashCardsCSVMaker
from ankit_api.users.utils import user_directory_path

from . import historical_records
from . import querysets


class Language(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    icon = models.FileField(verbose_name=_("Icon"), blank=True)
    history = simple_history_models.HistoricalRecords(related_name="history_log")

    class Meta:
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")

    def __str__(self):
        return f"{self.name}"


class StudySession(TimeStampedModel):
    name = models.CharField(max_length=64, verbose_name=_("Name"))
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
    language = simple_history_models.HistoricForeignKey(
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
    history = historical_records.StudySessionHistoricalRecords(
        related_name="history_log",
    )
    objects = querysets.StudySessionQuerySet.as_manager()

    class Meta:
        verbose_name = _("Study Session")
        verbose_name_plural = _("Study Sessions")

    def __str__(self):
        return f"{self.name} - {self.language} session of {self.user}"

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

    def update_duration(self):
        timezone = pytz.timezone(settings.TIME_ZONE)
        self.duration_in_minutes = datetime.now(tz=timezone) - self.created_at
        self.save()

    def update_cards_added(self):
        with Path.open(self.csv_file.path) as file:
            reader = csv.reader(file, delimiter=",")
            cards_count = sum(1 for row in reader)
            self.cards_added = cards_count
            self.save()

    def finish(self, cards_data):
        self.add_flaschards_file(cards_data)
        self.update_duration()
        self.update_cards_added()
        self.user.student.update_streak()
        self.user.student.update_total_study_time()
        self.user.student.save()
