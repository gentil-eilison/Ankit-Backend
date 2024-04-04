from django.utils.text import get_text_list
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion


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

    def get_card_for_word(self, word: str, language: str) -> None:
        prompt = (
            f"Você poderia criar um flashcard com a frente contendo a palavra "
            f"'{word}' do {language}, dentro de uma frase de exemplo, "
            "e a parte de trás contendo a tradução dessa frase em português, "
            f"dando destaque à palavra '{word}' e sua respectiva tradução?"
        )
        response = self.get_response_for(prompt)
        self.__current_response = response.choices[0].message.content

    def get_cards_by_topic(self, topic: str, language: str) -> None:
        prompt = (
            f"Você poderia criar no mínimo 10 flashcards com"
            f"vocabulário de {topic} "
            f"completo em {language}, com a frente contendo uma palavra"
            "desse tema em uma frase de exemplo, e a parte de trás "
            "contendo a tradução completa da frase em português, dando "
            "destaque à palavra e sua respectiva tradução?"
        )
        response = self.get_response_for(prompt)
        self.__current_response = response.choices[0].message.content
