from celery import shared_task

from .models import Student
from .models import User


@shared_task()
def validate_streak():
    users_who_didnt_study = User.objects.filter(student__studied_today=False)
    for user_to_validate_streak in users_who_didnt_study:
        try:
            student = user_to_validate_streak.student
            student.longest_streak = student.streak
            student.streak = 0
            student.save()
        except Student.DoesNotExist:
            continue
