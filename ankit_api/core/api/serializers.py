from dj_rest_auth.serializers import PasswordResetConfirmSerializer
from dj_rest_auth.serializers import PasswordResetSerializer
from django.contrib.auth.tokens import default_token_generator
from rest_framework import exceptions
from rest_framework import serializers

from ankit_api.users.forms import AnkitPasswordResetForm


class AnkitPasswordConfirmResetSerializer(PasswordResetConfirmSerializer):
    # Override necessary to remove "if 'allauth'" which caused the uid to be invalid
    def validate(self, attrs):
        from django.contrib.auth import get_user_model
        from django.utils.encoding import force_str
        from django.utils.http import urlsafe_base64_decode as uid_decoder
        from django.utils.translation import gettext_lazy as _

        UserModel = get_user_model()  # noqa: N806

        # Decode the uidb64 (allauth use base36) to uid to get User object
        try:
            uid = force_str(uid_decoder(attrs["uid"]))
            self.user = UserModel._default_manager.get(pk=uid)  # noqa: SLF001
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            raise exceptions.ValidationError({"uid": [_("Invalid value")]})  # noqa: B904

        if not default_token_generator.check_token(self.user, attrs["token"]):
            raise exceptions.ValidationError({"token": [_("Invalid value")]})

        self.custom_validation(attrs)
        # Construct SetPasswordForm instance
        self.set_password_form = self.set_password_form_class(
            user=self.user,
            data=attrs,
        )
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)

        return attrs


class AnkitPasswordResetSerializer(PasswordResetSerializer):
    @property
    def password_reset_form_class(self):
        return AnkitPasswordResetForm

    # Override necessary both to change email sent and set the token generator
    # to Django's one and not allauth's
    def get_email_options(self):
        return {
            "html_email_template_name": "email_reset_password.html",
            "token_generator": default_token_generator,
        }
