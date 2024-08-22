from django.core.exceptions import ObjectDoesNotExist
from simple_history.models import HistoricalRecords


class StudySessionHistoricalRecords(HistoricalRecords):
    def get_extra_fields(self, model, fields):
        extra_fields = super().get_extra_fields(model, fields)

        def custom_str(self):
            try:
                user_str = self.user.email
            except ObjectDoesNotExist:
                user_str = "unknown user"

            return f"{self.name} - {self.language} session of {user_str}"

        extra_fields["__str__"] = custom_str
        return extra_fields
