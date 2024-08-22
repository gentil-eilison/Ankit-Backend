from celery import shared_task
from django.db.models import F
from django.core import management

from .models import Student


@shared_task()
def validate_streak():
    students_who_didnt_study = Student.objects.filter(studied_today=False)
    students_who_didnt_study.update(longest_streak=F("streak"))
    students_who_didnt_study.update(streak=0)

@shared_task()
def backup_database():
    management.call_command('dbbackup')

@shared_task
def clean_old_database_files_and_backup():
    management.call_command('dbbackup --clean')

@shared_task
def restore_database():
    management.call_command('dbrestore') 

@shared_task
def backup_media_folder():   
    management.call_command('mediabackup')

@shared_task
def clean_old_media_folders_and_backup():
    management.call_command('mediabackup --clean')

@shared_task    
def restore_media_folder():    
    management.call_command('media_restore')
