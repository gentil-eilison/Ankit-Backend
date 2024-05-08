from celery import shared_task

from .models import Student
from .models import User


@shared_task()
def validate_streak():
    all_users = User.objects.all()
    for user_to_validate_streak in all_users:
        try:
            student = user_to_validate_streak.student

            if not student.studied_today:
                student.longest_streak = student.streak
                student.streak = 0
                student.save()
            else:
                student.streak += 1
                student.save()
        except Student.DoesNotExist:
            continue
