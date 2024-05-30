from django.dispatch import receiver
from simple_history.signals import post_create_historical_record

from .models import StudySession


@receiver(signal=post_create_historical_record, sender=StudySession.history.model)
def create_language_historical_record(instance, *args, **kwargs):
    # Needed because djangos-simple-history will register the change to
    # the historical table of the reverse foreign key
    instance.language.save()
