from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from simple_history.admin import SimpleHistoryAdmin

from ankit_api.core.admin import ModelLogAdmin

from .forms import UserAdminChangeForm
from .forms import UserAdminCreationForm
from .models import Nationality
from .models import Student
from .models import User

if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
    # Force the `admin` sign in process to go through the `django-allauth` workflow:
    # https://docs.allauth.org/en/latest/common/admin.html#admin
    admin.site.login = login_required(admin.site.login)  # type: ignore[method-assign]


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("name",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["email", "name", "is_superuser"]
    search_fields = ["name"]
    ordering = ["id"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )


@admin.register(Student)
class StudentHistoryAdmin(SimpleHistoryAdmin):
    list_display = [
        "id",
        "first_name",
        "last_name",
        "educational_level",
        "nationality",
        "profile_picture",
    ]
    history_list_display = ["status"]
    search_fields = ["first_name"]


class StudentLogAdmin(ModelLogAdmin):
    search_fields = ["first_name"]


admin.site.register(Student.history.model, StudentLogAdmin)
admin.site.register(Nationality)
