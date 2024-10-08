from drf_writable_nested.mixins import UniqueFieldsMixin
from drf_writable_nested.serializers import NestedUpdateMixin
from rest_framework import serializers

from ankit_api.users.models import Nationality
from ankit_api.users.models import Student
from ankit_api.users.models import User


class StudentSerializer(serializers.ModelSerializer[Student]):
    class Meta:
        model = Student
        fields = (
            "first_name",
            "last_name",
            "educational_level",
            "nationality",
            "profile_picture",
        )


class StudentReadSerializer(UniqueFieldsMixin, serializers.ModelSerializer[Student]):
    class Meta:
        model = Student
        fields = (
            "id",
            "first_name",
            "last_name",
            "profile_picture",
            "educational_level",
            "streak",
            "longest_streak",
            "nationality",
            "total_study_time",
            "user",
        )


class UserSerializer(NestedUpdateMixin):
    student = StudentReadSerializer(many=False)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "student",
        ]


class NationalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Nationality
        fields = ("id", "name")
