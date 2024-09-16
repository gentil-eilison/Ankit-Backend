from celery import shared_task
from django.contrib.auth import get_user_model
from django.core import management
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


@shared_task
def backup_database():
    management.call_command("dbbackup")


@shared_task
def clean_old_database_files_and_backup():
    management.call_command("dbbackup --clean")


@shared_task
def restore_database():
    management.call_command("dbrestore")


@shared_task
def backup_media_folder():
    management.call_command("mediabackup")


@shared_task
def clean_old_media_folders_and_backup():
    management.call_command("mediabackup --clean")


@shared_task
def restore_media_folder():
    management.call_command("media_restore")
