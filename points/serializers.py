"""
Сериализаторы для API точек и сообщений.
"""
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point as GeoPoint
from rest_framework import serializers

from .models import Message, Point


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя."""

    class Meta:
        model = User
        fields = ["id", "username"]
        read_only_fields = ["id", "username"]


class PointSerializer(serializers.ModelSerializer):
    """Сериализатор для точки."""

    latitude = serializers.FloatField(
        write_only=True,
        help_text="Широта точки",
    )
    longitude = serializers.FloatField(
        write_only=True,
        help_text="Долгота точки",
    )
    created_by = UserSerializer(read_only=True)
    messages_count = serializers.IntegerField(
        source="messages.count",
        read_only=True,
    )

    class Meta:
        model = Point
        fields = [
            "id",
            "name",
            "description",
            "latitude",
            "longitude",
            "location",
            "created_by",
            "created_at",
            "updated_at",
            "messages_count",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at", "location"]

    def create(self, validated_data: dict) -> Point:
        latitude = validated_data.pop("latitude")
        longitude = validated_data.pop("longitude")
        validated_data["location"] = GeoPoint(longitude, latitude, srid=4326)
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)

    def to_representation(self, instance: Point) -> dict:
        representation = super().to_representation(instance)
        if instance.location:
            representation["latitude"] = instance.latitude
            representation["longitude"] = instance.longitude
        return representation


class MessageSerializer(serializers.ModelSerializer):
    """Сериализатор для сообщения."""

    author = UserSerializer(read_only=True)
    point_id = serializers.IntegerField(
        write_only=True,
        help_text="ID точки, к которой относится сообщение",
    )

    class Meta:
        model = Message
        fields = [
            "id",
            "point_id",
            "point",
            "text",
            "author",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "point", "author", "created_at", "updated_at"]

    def create(self, validated_data: dict) -> Message:
        point_id = validated_data.pop("point_id")
        try:
            point = Point.objects.get(id=point_id)
        except Point.DoesNotExist:
            raise serializers.ValidationError({"point_id": "Точка с указанным ID не найдена"})
        validated_data["point"] = point
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)

    def to_representation(self, instance: Message) -> dict:
        representation = super().to_representation(instance)
        representation["point"] = PointSerializer(instance.point).data
        return representation


class PointSearchSerializer(serializers.Serializer):
    """Сериализатор для поиска точек в радиусе."""

    latitude = serializers.FloatField(
        help_text="Широта центра поиска",
    )
    longitude = serializers.FloatField(
        help_text="Долгота центра поиска",
    )
    radius = serializers.FloatField(
        help_text="Радиус поиска в километрах",
        min_value=0.1,
        max_value=1000,
    )


class MessageSearchSerializer(serializers.Serializer):
    """Сериализатор для поиска сообщений в радиусе."""

    latitude = serializers.FloatField(
        help_text="Широта центра поиска",
    )
    longitude = serializers.FloatField(
        help_text="Долгота центра поиска",
    )
    radius = serializers.FloatField(
        help_text="Радиус поиска в километрах",
        min_value=0.1,
        max_value=1000,
    )
