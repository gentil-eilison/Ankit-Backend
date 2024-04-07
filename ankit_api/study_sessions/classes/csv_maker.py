import csv
import uuid
from pathlib import Path

from .anki_card import AnkiCard


class FlashCardsCSVMaker:
    def __init__(self, cards: tuple[AnkiCard]):
        self.__cards = cards
        self.__filename = f"flashcards-{uuid.uuid4().hex}.csv"

    @property
    def cards(self) -> tuple[AnkiCard]:
        return self.__cards

    @property
    def filename(self) -> str:
        return self.__filename

    @filename.setter
    def filename(self, new_filename: str) -> None:
        self.__filename = new_filename

    def generate_csv(self) -> None:
        with Path.open(self.__filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for card in self.__cards:
                writer.writerow([card.front, card.back])

    def clean(self):
        Path.unlink(self.__filename)
