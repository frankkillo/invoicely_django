from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import TeamViewSet

app_name = 'teams'

router = DefaultRouter()
router.register('teams', TeamViewSet)
urlpatterns = [
    path('', include(router.urls))
]