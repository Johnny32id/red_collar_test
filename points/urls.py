"""
URL маршруты для API точек и сообщений.
"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MessageViewSet, PointViewSet

router = DefaultRouter()
router.register(r"points", PointViewSet, basename="point")
router.register(r"messages", MessageViewSet, basename="message")

urlpatterns = [
    path("", include(router.urls)),
]
