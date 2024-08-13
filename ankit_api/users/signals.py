from django.contrib.auth import get_user_model
from django.dispatch import receiver
from simple_history.signals import pre_create_historical_record

from ankit_api.core.models import get_sentinel_user

from .models import Student

User = get_user_model()


@receiver(signal=pre_create_historical_record, sender=Student.history.model)
def set_historical_student_history_user(instance, *args, **kwargs):
    history_instance = kwargs.get("history_instance")
    history_instance.history_user = get_sentinel_user()


@receiver(signal=pre_create_historical_record, sender=User.history.model)
def clean_historical_user_history_user(instance, *args, **kwargs):
    instance.history.all().update(history_user=get_sentinel_user())
    history_instance = kwargs.get("history_instance")
    history_instance.history_user = get_sentinel_user()
