"""
Тесты для моделей и API точек и сообщений.
"""
import pytest
from django.contrib.gis.geos import Point as GeoPoint
from rest_framework import status

from points.models import Message, Point


@pytest.mark.django_db
class TestPointModel:
    def test_create_point(self, user):
        location = GeoPoint(37.6173, 55.7558, srid=4326)
        point = Point.objects.create(
            name="Москва",
            description="Столица России",
            location=location,
            created_by=user,
        )
        assert point.name == "Москва"
        assert point.latitude == 55.7558
        assert point.longitude == 37.6173
        assert point.created_by == user

    def test_point_str(self, point):
        assert "Тестовая точка" in str(point)
        assert str(point.latitude) in str(point)
        assert str(point.longitude) in str(point)


@pytest.mark.django_db
class TestMessageModel:
    def test_create_message(self, point, user):
        message = Message.objects.create(
            point=point,
            text="Привет из Москвы!",
            author=user,
        )
        assert message.text == "Привет из Москвы!"
        assert message.point == point
        assert message.author == user

    def test_message_str(self, message):
        assert message.author.username in str(message)
        assert message.point.name in str(message)


@pytest.mark.django_db
class TestPointAPI:
    def test_create_point_unauthorized(self, api_client):
        response = api_client.post(
            "/api/points/",
            {
                "name": "Новая точка",
                "latitude": 55.7558,
                "longitude": 37.6173,
            },
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_point_authorized(self, authenticated_api_client, user):
        response = authenticated_api_client.post(
            "/api/points/",
            {
                "name": "Новая точка",
                "description": "Описание",
                "latitude": 55.7558,
                "longitude": 37.6173,
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "Новая точка"
        assert response.data["latitude"] == 55.7558
        assert response.data["longitude"] == 37.6173
        assert response.data["created_by"]["username"] == user.username

    def test_list_points(self, authenticated_api_client, point):
        response = authenticated_api_client.get("/api/points/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1

    def test_search_points_in_radius(self, authenticated_api_client, point):
        response = authenticated_api_client.get(
            "/api/points/search/",
            {
                "latitude": 55.7558,
                "longitude": 37.6173,
                "radius": 10,
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_search_points_outside_radius(self, authenticated_api_client, point):
        response = authenticated_api_client.get(
            "/api/points/search/",
            {
                "latitude": 59.9343,
                "longitude": 30.3351,
                "radius": 1,
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0


@pytest.mark.django_db
class TestMessageAPI:
    def test_create_message_unauthorized(self, api_client, point):
        response = api_client.post(
            "/api/points/messages/",
            {
                "point_id": point.id,
                "text": "Новое сообщение",
            },
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_message_authorized(self, authenticated_api_client, point, user):
        response = authenticated_api_client.post(
            "/api/points/messages/",
            {
                "point_id": point.id,
                "text": "Новое сообщение",
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["text"] == "Новое сообщение"
        assert response.data["author"]["username"] == user.username
        assert response.data["point"]["id"] == point.id

    def test_create_message_invalid_point(self, authenticated_api_client):
        response = authenticated_api_client.post(
            "/api/points/messages/",
            {
                "point_id": 99999,
                "text": "Сообщение",
            },
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_list_messages(self, authenticated_api_client, message):
        response = authenticated_api_client.get("/api/messages/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) >= 1

    def test_search_messages_in_radius(self, authenticated_api_client, point, message):
        response = authenticated_api_client.get(
            "/api/messages/search/",
            {
                "latitude": 55.7558,
                "longitude": 37.6173,
                "radius": 10,
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_search_messages_outside_radius(self, authenticated_api_client, point, message):
        response = authenticated_api_client.get(
            "/api/messages/search/",
            {
                "latitude": 59.9343,
                "longitude": 30.3351,
                "radius": 1,
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0
