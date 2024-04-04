class AnkiCard:
    def __init__(self, front: str, back: str, audio_filename: str):
        self.__front = front
        self.__back = back
        self.__audio_filename = audio_filename

    @property
    def front(self) -> str:
        return self.__front

    @front.setter
    def front(self, new_front: str) -> None:
        self.__front = new_front

    @property
    def back(self) -> str:
        return self.__back

    @back.setter
    def back(self, new_back: str) -> None:
        self.__back = new_back

    @property
    def audio_filename(self) -> str:
        return self.__audio_filename

    @audio_filename.setter
    def audio_filename(self, new_audio_filename: str) -> None:
        self.__audio_filename = new_audio_filename
