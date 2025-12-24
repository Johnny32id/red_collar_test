"""
URL маршруты для API точек и сообщений.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PointViewSet, MessageViewSet

router = DefaultRouter()
router.register(r"points", PointViewSet, basename="point")
router.register(r"messages", MessageViewSet, basename="message")

urlpatterns = [
    path("", include(router.urls)),
]

