from django.apps import apps
from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete
from django.dispatch import receiver


@receiver(signal=post_delete, sender=get_user_model())
def set_history_user_to_null_on_user_deletion(sender, instance, **kwargs):
    historical_models = [
        model for model in apps.get_models() if hasattr(model, "history_user")
    ]

    for historical_model in historical_models:
        historical_model.objects.filter(history_user=instance).update(history_user=None)
