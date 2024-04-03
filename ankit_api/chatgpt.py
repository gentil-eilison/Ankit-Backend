from django.utils.text import get_text_list
from openai import OpenAI
from openai.types.chat.chat_completion import Choice


class ChatGPT:
    MODELS: tuple[str] = (
        "gpt-4",
        "gpt-3.5-turbo",
    )

    def __init__(self, model: str = "gpt-3.5-turbo") -> None:
        self.__model: str = self.__set_model(model)
        self.__client = OpenAI()
        self.__current_response: list[Choice] = []

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
    def current_response(self) -> list[Choice]:
        return self.__current_response

    @model.setter
    def model(self, new_model: str) -> None:
        self.__model = new_model

    def get_card_for_word(self, word: str, language: str) -> None:
        prompt = (
            f"Você poderia criar um flashcard com a frente contendo a palavra "
            f"'{word}' do {language}, dentro de uma frase de exemplo, "
            "e a parte de trás contendo a tradução dessa frase em português, "
            f"dando destaque à palavra '{word}' e sua respectiva tradução?"
        )
        response = self.client.chat.completions.create(
            model=self.__model,
            messages=[
                {"role": "user", "content": prompt},
            ],
        )
        self.__current_response = response.choices
