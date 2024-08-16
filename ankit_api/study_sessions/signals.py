from django.dispatch import receiver
from simple_history.signals import post_create_historical_record
from simple_history.signals import pre_create_historical_record

from ankit_api.core.models import get_sentinel_user

from .models import Language
from .models import StudySession


@receiver(signal=post_create_historical_record, sender=StudySession.history.model)
def create_language_historical_record(instance, *args, **kwargs):
    # Needed because djangos-simple-history will register the change to
    # the historical table of the reverse foreign key
    instance.language.save()


@receiver(signal=pre_create_historical_record, sender=StudySession.history.model)
def set_historical_study_session_history_user(instance, *args, **kwargs):
    instance.history.all().update(history_user=get_sentinel_user())
    history_instance = kwargs.get("history_instance")
    history_instance.history_user = get_sentinel_user()


@receiver(signal=pre_create_historical_record, sender=Language.history.model)
def set_historical_language_history_user(instance, *args, **kwargs):
    instance.history.all().update(history_user=get_sentinel_user())
    history_instance = kwargs.get("history_instance")
    history_instance.history_user = get_sentinel_user()
