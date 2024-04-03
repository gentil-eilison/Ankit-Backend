from .models import StudySession
from rest_framework import serializers


class StudySessionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StudySession
        fields = ['duration_in_minutes', 'cards_added',
                  'spreadsheet_file', 'language', 'user']
