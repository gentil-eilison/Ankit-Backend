from django.core.management.base import BaseCommand
from django.db import IntegrityError

from ankit_api.users.models import Nationality
from ankit_api.users.models import Student
from ankit_api.users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options) -> str | None:
        try:
            user = User.objects.create_user(
                email="cplusplususer@gmail.com",
                password="123456",  # noqa: S106
                is_superuser=True,
                is_staff=True,
            )
            Student.objects.get_or_create(
                first_name="John",
                last_name="Doe",
                nationality=Nationality.objects.get(name="Indiano"),
                user=user,
            )
            self.stdout.write(
                self.style.SUCCESS("Initial admin user created successfully!"),
            )
        except IntegrityError:
            self.stdout.write(self.style.WARNING("Admin user already created"))
