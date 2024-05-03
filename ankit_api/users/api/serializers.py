from drf_writable_nested.mixins import UniqueFieldsMixin
from drf_writable_nested.serializers import NestedUpdateMixin
from rest_framework import serializers

from ankit_api.users.models import Student
from ankit_api.users.models import User


class StudentSerializer(serializers.ModelSerializer[Student]):
    class Meta:
        model = Student
        fields = ("first_name", "last_name", "educational_level", "nationality")


class StudentReadSerializer(UniqueFieldsMixin, serializers.ModelSerializer[Student]):
    class Meta:
        model = Student
        fields = (
            "first_name",
            "last_name",
            "educational_level",
            "streak",
            "longest_streak",
            "nationality",
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
