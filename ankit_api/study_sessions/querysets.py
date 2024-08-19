from django.db import models


class StudySessionQuerySet(models.QuerySet):
    def by_user(self, user):
        return self.filter(user=user)
