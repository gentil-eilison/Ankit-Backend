import re, uuid

from pathlib import Path
from django.conf import settings
from django.utils.text import get_text_list
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion

from ankit_api.study_sessions.classes.anki_card import AnkiCard


class ChatGPT:
    MODELS: tuple[str] = (
        "gpt-4",
        "gpt-3.5-turbo",
    )

    def __init__(self, model: str = "gpt-3.5-turbo") -> None:
        self.__model: str = self.__set_model(model)
        self.__client = OpenAI()
        self.__current_response: str = []

    def __set_model(self, model: str) -> str:
        if model not in self.MODELS:
            valid_values = get_text_list(self.MODELS, "and")
            exception_msg = f"Invalid model name. Valid values are: {valid_values}"
            raise ValueError(exception_msg)
        return model

    @property
    def client(self) -> OpenAI:
        return self.__client

    @client.setter
    def client(self, new_client: OpenAI) -> None:
        self.__client = new_client

    @property
    def model(self) -> str:
        return self.__model

    @property
    def current_response(self) -> str:
        return self.__current_response

    @model.setter
    def model(self, new_model: str) -> None:
        self.__model = new_model

    def get_response_for(self, prompt: str) -> ChatCompletion:
        return self.client.chat.completions.create(
            model=self.__model,
            messages=[
                {"role": "user", "content": prompt},
            ],
        )

    def generate_audio_for_phrase(self, phrase: str) -> Path:
        speech_file_path = Path(settings.TTS_SPEECH_FILES_DIR + f"/audio-{uuid.uuid4().hex}")  
        audio_phrase = self.__client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=phrase
        )

        audio_phrase.stream_to_file(speech_file_path)
        return speech_file_path.absolute()

    def get_card_for_word(self, word: str, language: str) -> None:
        prompt = (
            "Crie uma flashcard com a seguinte estrutura: \n"
            f"Frente: frase em {language} com a palavra {word} dentro da frase\n"
            f"Verso: tradução da frase que está na frente para o português"
        )
        response = self.get_response_for(prompt)
        self.__current_response = response.choices[0].message.content

    def get_cards_by_topic(
        self,
        topic: str,
        language: str,
        cards_count: int = 10,
    ) -> None:
        prompt = (
            f"Você poderia criar no mínimo {cards_count} flashcards"
            f"com vocabulário de {topic} completo em {language}, com"
            f"a frente contendo o texto 'Frente:' e o conteúdo sendo"
            "uma frase de exemplo, e o verso contendo o texto 'Verso:'"
            "e a exatamente mesma frase completa do exemplo da frente, "
            "mas em português?"
        )
        response = self.get_response_for(prompt)
        self.__current_response = response.choices[0].message.content

    def generate_cards(self) -> list[AnkiCard]:
        cards = []
        fronts: list[str] = re.findall(r"(?<=Frente:) .+", self.__current_response)
        backs: list[str] = re.findall(r"(?<=Verso:) .+", self.__current_response)
        front_back_pairs = zip(fronts, backs, strict=False)

        for front, back in front_back_pairs:
            audio_path = self.generate_audio_for_phrase(front)
            cards.append(AnkiCard(front=front.strip(), back=back.strip(), audio_filename=audio_path))
        return cards