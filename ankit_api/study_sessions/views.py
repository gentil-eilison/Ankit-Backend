from operator import itemgetter

from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from ankit_api.chatgpt import ChatGPT

from .models import Language
from .models import StudySession
from .serializers import StudySessionSerializer
from .serializers import VocabularyBuilderSerializer


class VocabularyBuilderView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        vocabulary_builder_serializer = VocabularyBuilderSerializer(data=request.data)
        if vocabulary_builder_serializer.is_valid():
            topic, language, vocabulary = itemgetter("topic", "language", "name")(
                vocabulary_builder_serializer.data,
            )
            language = Language.objects.get(id=language)
            client = ChatGPT()
            if topic:
                client.get_cards_by_topic(vocabulary, language.name)
            else:
                client.get_card_for_word(vocabulary, language.name)
            cards_text = client.current_response
            return Response(
                status=status.HTTP_201_CREATED,
                data={"cards_text": cards_text},
            )
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data=vocabulary_builder_serializer.errors,
        )


class StudySessionViewSet(viewsets.ModelViewSet):
    queryset = StudySession.objects.all()
    serializer_class = StudySessionSerializer
    permission_classes = (permissions.IsAuthenticated,)
