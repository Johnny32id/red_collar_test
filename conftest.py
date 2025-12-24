"""
Конфигурация pytest для проекта.
"""
import pytest
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point as GeoPoint

from points.models import Message, Point


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="testuser",
        password="testpass123",
        email="test@example.com",
    )


@pytest.fixture
def another_user(db):
    return User.objects.create_user(
        username="anotheruser",
        password="testpass123",
        email="another@example.com",
    )


@pytest.fixture
def point(user, db):
    location = GeoPoint(37.6173, 55.7558, srid=4326)
    return Point.objects.create(
        name="Тестовая точка",
        description="Описание тестовой точки",
        location=location,
        created_by=user,
    )


@pytest.fixture
def message(point, user, db):
    return Message.objects.create(
        point=point,
        text="Тестовое сообщение",
        author=user,
    )


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def authenticated_api_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client
