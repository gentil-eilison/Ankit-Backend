from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter
from ankit_api.study_sessions.views import StudySessionViewSet

from ankit_api.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register(r'study_sessions', StudySessionViewSet)


app_name = "api"
urlpatterns = router.urls
