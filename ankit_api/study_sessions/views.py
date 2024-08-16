from operator import itemgetter

from rest_framework import pagination
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.views import APIView

from ankit_api.chatgpt import ChatGPT

from .api import filtersets
from .models import Language
from .models import StudySession
from .serializers import AnkiCardSerializer
from .serializers import LanguageSerializer
from .serializers import StudySessionReadSerializer
from .serializers import StudySessionSerializer
from .serializers import VocabularyBuilderSerializer


class VocabularyBuilderView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        vocabulary_builder_serializer = VocabularyBuilderSerializer(data=request.data)
        if vocabulary_builder_serializer.is_valid():
            topic, name, language, cards_count, card_type = itemgetter(
                "topic",
                "name",
                "language",
                "cards_count",
                "card_type",
            )(
                vocabulary_builder_serializer.data,
            )
            client = ChatGPT()
            language = Language.objects.get(id=language)
            if topic:
                client.get_cards_by_topic(name, language.name, card_type, cards_count)
            else:
                client.get_card_for_word(name, language.name, card_type)
            cards = client.generate_cards()
            cards_serializer = AnkiCardSerializer(cards, many=True)
            return Response(
                status=status.HTTP_200_OK,
                data={"cards": cards_serializer.data},
            )
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data=vocabulary_builder_serializer.errors,
        )


class StudySessionViewSet(viewsets.ModelViewSet):
    queryset = StudySession.objects.none()
    serializer_class = StudySessionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filterset_class = filtersets.StudySessionFilter
    pagination_class = pagination.PageNumberPagination
    http_method_names = ("get", "post", "delete")

    def get_queryset(self, *args, **kwargs):
        return StudySession.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self) -> type[BaseSerializer]:
        if self.request.method == "GET":
            return StudySessionReadSerializer
        return super().get_serializer_class()

    @action(methods=["post"], detail=True)
    def finish(self, request, pk=None):
        study_session: StudySession = self.get_object()
        print("olha essa porra aqui")
        print(study_session.csv_file)
        if not study_session.csv_file:
            cards_serializer = AnkiCardSerializer(data=request.data, many=True)
            cards_serializer.is_valid(raise_exception=True)
            study_session.finish(cards_data=cards_serializer.data)
            response_csv_file = self.get_serializer_class()(study_session)
            return Response(data=response_csv_file.data, status=status.HTTP_200_OK)
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={"error": "Study session already finished"},
        )


class LanguagesListView(ListAPIView):
    queryset = Language.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = LanguageSerializer
