import re

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
        self.__card_types: dict[str] = {
            "basic": "a tradução da frase que está na frente para o português",
            "intermediate": "a palavra a qual foi solicitada a tradução, seguido de sua"
            "tradução, nessa estrutura: palavra: tradução da palavra",
            "advanced": "a palavra a qual foi solicitada a tradução, seguido de sua"
            "definição no idioma, na seguinte estrutura: palavra: significado da"
            "palavra em",
        }

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

    def handle_card_type_string(
        self,
        card_type: str,
        language: str,
        is_topic,
    ) -> str:
        if card_type == "advanced":
            if is_topic:
                return (
                    f"{self.__card_types[card_type]} {language}, sendo que o termo "
                    "'palavra' se refere à palavra da frase que faz parte do tópico "
                    "que pedi"
                )
            return f"{self.__card_types[card_type]} {language}"
        if card_type == "intermediate" and is_topic:
            return (
                f"{self.__card_types[card_type]}, sendo que 'palavra' se refere ao "
                "termo da frase que faz parte do tópico que pedi"
            )
        return f"{self.__card_types[card_type]}"

    def get_card_for_word(self, word: str, language: str, card_type: str) -> None:
        verse_card_prompt = self.handle_card_type_string(
            card_type,
            language,
            is_topic=False,
        )
        prompt = (
            "Crie uma flashcard com a seguinte estrutura: \n"
            f"Frente: frase em {language} com a palavra {word} dentro da frase\n"
            f"Verso: {verse_card_prompt}"
        )
        response = self.get_response_for(prompt)
        self.__current_response = response.choices[0].message.content

    def get_cards_by_topic(
        self,
        topic: str,
        language: str,
        card_type: str,
        cards_count: int = 10,
    ) -> None:
        verse_card_prompt = self.handle_card_type_string(
            card_type,
            language,
            is_topic=True,
        )
        prompt = (
            f"Você poderia criar no mínimo {cards_count} flashcards"
            f"com vocabulário de {topic} completo em {language}, com"
            f"a frente contendo o texto 'Frente:' e o conteúdo sendo"
            f"uma frase de exemplo, e o verso contendo o texto 'Verso:'"
            f"com {verse_card_prompt}. Só pode haver uma palavra do tópico por frase."
        )
        response = self.get_response_for(prompt)
        self.__current_response = response.choices[0].message.content

    def generate_cards(self) -> list[AnkiCard]:
        cards = []
        fronts: list[str] = re.findall(r"(?<=Frente:) .+", self.__current_response)
        backs: list[str] = re.findall(r"(?<=Verso:) .+", self.__current_response)
        front_back_pairs = zip(fronts, backs, strict=False)

        for front, back in front_back_pairs:
            cards.append(
                AnkiCard(
                    front=front.strip(),
                    back=back.strip(),
                ),
            )
        return cards
