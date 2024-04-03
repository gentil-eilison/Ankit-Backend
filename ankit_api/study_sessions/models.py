from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history import models as simple_history_models


class Language(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    icon = models.FileField(verbose_name=_("Icon"))
    history = simple_history_models.HistoricalRecords()

    class Meta:
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")

    def __str__(self):
        return f"{self.name}"
