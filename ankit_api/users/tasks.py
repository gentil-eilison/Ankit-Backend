from datetime import datetime

from celery import shared_task
from django.conf import settings

from ankit_api.study_sessions.models import StudySession

from .models import Student
from .models import User


@shared_task()
def validate_streak():
    all_users = User.objects.all()
    for user_to_validate_streak in all_users:
        user_study_sessions = StudySession.objects.filter(user=user_to_validate_streak)
        last_study_session_datetime = user_study_sessions.latest().created_at

        last_study_session_date = last_study_session_datetime.date()
        current_date = datetime.now(tz=settings.TIME_ZONE).date()
        date_diff = current_date - last_study_session_date
        diff_in_days = date_diff.days

        if diff_in_days > 1:
            student = Student.objects.get(user=user_to_validate_streak)
            student.longest_streak = student.streak
            student.streak = 0
            student.save()
