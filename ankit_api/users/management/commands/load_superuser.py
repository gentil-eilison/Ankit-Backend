from django.core.management.base import BaseCommand

from ankit_api.users.models import Nationality
from ankit_api.users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options) -> str | None:
        self.stdout.write(self.style.SUCCESS("Creating test data..."))
        User.objects.create_user(
            email="cplusplususer@gmail.com",
            password="123456",  # noqa: S106
            first_name="John",
            last_name="Doe",
            nationality=Nationality.objects.get(name="Indiano"),
            is_superuser=True,
            is_staff=True,
        )
        self.stdout.write(
            self.style.SUCCESS("Initial admin user created successfully!"),
        )
