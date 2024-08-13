from django.contrib.auth import get_user_model
from django.db import models


def get_sentinel_user():
    User = get_user_model()  # noqa: N806
    sentinel_user, _ = User.objects.get_or_create(email="sentinel@dummy.com")
    return sentinel_user


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
