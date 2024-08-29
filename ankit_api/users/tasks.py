from celery import shared_task
from django.contrib.auth import get_user_model
from django.db.models import F

from .models import Student


@shared_task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    User = get_user_model()  # noqa: N806
    return User.objects.count()


@shared_task()
def validate_streak():
    students_who_didnt_study = Student.objects.filter(studied_today=False)
    students_who_didnt_study.update(longest_streak=F("streak"))
    students_who_didnt_study.update(streak=0)
