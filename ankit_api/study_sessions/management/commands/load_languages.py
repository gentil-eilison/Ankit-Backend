from django.core.management.base import BaseCommand

from ankit_api.study_sessions.models import Language


class Command(BaseCommand):
    help = "Creates languages"

    def handle(self, *args, **options) -> str | None:
        languages = (
            "Inglês",
            "Francês",
            "Espanhol",
            "Alemão",
            "Italiano",
            "Dinamarquês",
            "Finlandês",
            "Ucraniano",
            "Russo",
            "Chinês (Mandarim)",
            "Coreano",
            "Japonês",
            "Sueco",
        )

        for language in languages:
            Language.objects.get_or_create(name=language)

        self.stdout.write(
            self.style.SUCCESS("Languages successfully populated into the database."),
        )
