from rest_framework import serializers

from ankit_api.users.models import Student
from ankit_api.users.models import User


class StudentSerializer(serializers.ModelSerializer[Student]):
    class Meta:
        model = Student
        fields = ("first_name", "last_name", "educational_level", "nationality")


class StudentReadSerializer(serializers.ModelSerializer[Student]):
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


class UserSerializer(serializers.ModelSerializer[User]):
    student = StudentReadSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = [
            "url",
            "email",
            "student",
        ]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }
