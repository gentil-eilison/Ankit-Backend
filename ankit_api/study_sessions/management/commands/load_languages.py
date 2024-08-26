from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from ankit_api.study_sessions.models import Language


class Command(BaseCommand):
    help = "Creates languages"

    def handle(self, *args, **options) -> str | None:
        languages = (
            ("Inglês", "united_states_of_america.png"),
            ("Francês", "france.png"),
            ("Espanhol", "spain.png"),
            ("Alemão", "germany.png"),
            ("Italiano", "italy.png"),
            ("Dinamarquês", "denmark.png"),
            ("Finlandês", "finland.png"),
            ("Ucraniano", "ukraine.png"),
            ("Russo", "russia.png"),
            ("Chinês (Mandarim)", "china.png"),
            ("Coreano", "south_korea.png"),
            ("Japonês", "japan.png"),
            ("Sueco", "sweden.png"),
        )

        for name, lang_flag in languages:
            flag = Path(
                settings.BASE_DIR / "ankit_api" / "static" / "images" / f"{lang_flag}",
            )
            with flag.open("rb") as file:
                Language.objects.update_or_create(
                    name=name,
                    defaults={"name": name, "icon": File(file, flag.name)},
                )

        self.stdout.write(
            self.style.SUCCESS("Languages successfully populated into the database."),
        )
