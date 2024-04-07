from operator import itemgetter

from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from ankit_api.chatgpt import ChatGPT
from ankit_api.study_sessions.models import Language

from .models import StudySession
from .serializers import AnkiCardSerializer
from .serializers import StudySessionSerializer
from .serializers import VocabularyBuilderSerializer


class VocabularyBuilderView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        vocabulary_builder_serializer = VocabularyBuilderSerializer(data=request.data)
        if vocabulary_builder_serializer.is_valid():
            topic, name, language, cards_count = itemgetter(
                "topic",
                "name",
                "language",
                "cards_count",
                "text_to_speech",
            )(
                vocabulary_builder_serializer.data,
            )
            client = ChatGPT()
            language = Language.objects.get(id=language)
            if topic:
                client.get_cards_by_topic(name, language.name, cards_count)
            else:
                client.get_card_for_word(name, language.name)
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
    queryset = StudySession.objects.all()
    serializer_class = StudySessionSerializer
    permission_classes = (permissions.IsAuthenticated,)
