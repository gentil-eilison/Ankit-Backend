from datetime import timedelta
from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from simple_history import models as simple_history_models

from ankit_api.core.models import TimeStampedModel
from ankit_api.utils.upload_to_funcs import user_directory_path

from .managers import UserManager


class Nationality(TimeStampedModel):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    history = simple_history_models.HistoricalRecords(related_name="history_log")

    class Meta:
        verbose_name = _("Nationality")
        verbose_name_plural = _("Nationalities")

    def __str__(self):
        return self.name


class User(AbstractUser):
    """
    Default custom user model for ankit_api.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    email = models.EmailField(_("email address"), unique=True)
    username = None  # type: ignore[assignment]
    history = simple_history_models.HistoricalRecords(related_name="history_log")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self) -> str:
        return reverse("users:detail", kwargs={"pk": self.id})


class Student(TimeStampedModel):
    class EducationalLevels(models.TextChoices):
        MIDDLE_SCHOOL = "Middle School", _("Ensino Fundamental")
        HIGH_SCHOOL = "High School", _("Ensino Médio")
        UNIVERSITY = "University", _("Superior")

    first_name = models.CharField(max_length=255, verbose_name=_("First name"))
    last_name = models.CharField(max_length=255, verbose_name=_("Last name"))

    educational_level = models.CharField(
        max_length=13,
        choices=EducationalLevels.choices,
        verbose_name=_("Educational level"),
    )
    streak = models.PositiveSmallIntegerField(verbose_name=_("Streak"), default=0)
    longest_streak = models.PositiveSmallIntegerField(
        verbose_name=_("Longest streak"),
        default=0,
    )
    nationality = models.ForeignKey(
        Nationality,
        related_name="users",
        on_delete=models.PROTECT,
        verbose_name=_("Nationality"),
    )
    studied_today = models.BooleanField(verbose_name=_("Studied today"), default=False)
    total_study_time = models.DurationField(
        verbose_name=_("Total study time"),
        default=timedelta(minutes=0),
    )
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        verbose_name=_("User"),
        related_name="student",
    )
    profile_picture = models.ImageField(
        verbose_name=_("Profile picture"),
        upload_to=user_directory_path,
        blank=True,
    )
    history = simple_history_models.HistoricalRecords(related_name="history_log")

    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Students")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def update_streak(self):
        if not self.studied_today:
            self.streak += 1
            self.studied_today = True
            self.save()

    # Mover também para o queryset de StudySessions

    def update_total_study_time(self):
        self.total_study_time = self.user.study_sessions.aggregate(
            models.Sum("duration_in_minutes"),
        )["duration_in_minutes__sum"]
