from rest_framework import serializers

from .models import Language
from .models import StudySession


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ("id", "name", "icon")


class StudySessionsByLanguageSerializer(serializers.ModelSerializer):
    study_sessions_count = serializers.SerializerMethodField(
        method_name="get_study_sessions_count",
    )
    name = serializers.SerializerMethodField(method_name="get_name")

    class Meta:
        model = Language.history.model
        fields = ("id", "name", "study_sessions_count")

    def get_study_sessions_count(self, language):
        return language.instance.study_sessions.count()

    def get_name(self, language):
        return Language.objects.get(id=language.id).name


class CardsAddedByLanguageSerializer(serializers.ModelSerializer):
    cards_added = serializers.SerializerMethodField(method_name="get_cards_added")

    class Meta:
        model = Language
        fields = ("id", "name", "cards_added")

    def get_cards_added(self, language):
        return language.cards_added_count()


class StudySessionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = StudySession
        fields = (
            "id",
            "duration_in_minutes",
            "cards_added",
            "csv_file",
            "language",
            "user",
        )


class AnkiCardSerializer(serializers.Serializer):
    front = serializers.CharField(max_length=128)
    back = serializers.CharField(max_length=128)


class VocabularyBuilderSerializer(serializers.Serializer):
    card_type_choices = ("basic", "intermediate", "advanced")

    topic = serializers.BooleanField(default=False)
    name = serializers.CharField(max_length=255)
    language = serializers.PrimaryKeyRelatedField(queryset=Language.objects.all())
    cards_count = serializers.IntegerField(min_value=1, max_value=20, default=10)
    card_type = serializers.ChoiceField(card_type_choices)
