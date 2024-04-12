from rest_framework import serializers

from .models import Language
from .models import StudySession


class StudySessionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StudySession
        fields = (
            "duration_in_minutes",
            "cards_added",
            "spreadsheet_file",
            "language",
            "user",
        )


class AnkiCardSerializer(serializers.Serializer):
    front = serializers.CharField(max_length=128)
    back = serializers.CharField(max_length=128)


class VocabularyBuilderSerializer(serializers.Serializer):
    topic = serializers.BooleanField(default=False)
    name = serializers.CharField(max_length=255)
    language = serializers.PrimaryKeyRelatedField(queryset=Language.objects.all())
    cards_count = serializers.IntegerField(min_value=1, max_value=20, default=10)
