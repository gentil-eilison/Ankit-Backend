from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from ankit_api.core.api.utils import get_api_urls
from ankit_api.study_sessions.api.views import StudySessionViewSet
from ankit_api.users.api import views as users_views

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", users_views.UserViewSet)
router.register(r"study_sessions", StudySessionViewSet)


app_name = "api"
urlpatterns = router.urls
urlpatterns += get_api_urls()
