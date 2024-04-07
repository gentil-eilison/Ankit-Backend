import csv
from pathlib import Path

from .anki_card import AnkiCard


class FlashCardsCSVMaker:
    def __init__(self, cards: tuple[AnkiCard], filename=""):
        self.__cards = cards
        self.__filename = filename

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
        with Path.open("flah_cards.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for card in self.__cards:
                writer.writerow([card.front, card.back])
