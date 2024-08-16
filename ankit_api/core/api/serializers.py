from dj_rest_auth.serializers import PasswordResetSerializer
from django.contrib.auth.forms import PasswordResetForm


class AnkitPasswordResetSerializer(PasswordResetSerializer):
    @property
    def password_reset_form_class(self):
        return PasswordResetForm

    def get_email_options(self):
        return {
            "html_email_template_name": "email_reset_password.html",
        }
