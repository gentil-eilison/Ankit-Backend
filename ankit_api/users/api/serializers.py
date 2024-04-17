from rest_framework import serializers

from ankit_api.users.models import User


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "url",
            "email",
            "educational_level",
            "streak",
            "longest_streak",
            "nationality",
        ]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }
