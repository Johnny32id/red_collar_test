"""
API представления для работы с точками и сообщениями.
"""
from django.contrib.gis.geos import Point as GeoPoint
from django.contrib.gis.measure import D
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Point, Message
from .serializers import (
    PointSerializer,
    MessageSerializer,
    PointSearchSerializer,
    MessageSearchSerializer,
)


class PointViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с точками."""

    queryset = Point.objects.all()
    serializer_class = PointSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related("created_by").prefetch_related("messages")
        return queryset

    @action(
        detail=False,
        methods=["post"],
        url_path="messages",
        serializer_class=MessageSerializer,
    )
    def create_message(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        return Response(
            MessageSerializer(message).data,
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=False,
        methods=["get"],
        url_path="search",
        serializer_class=PointSearchSerializer,
    )
    def search(self, request):
        serializer = PointSearchSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        latitude = serializer.validated_data["latitude"]
        longitude = serializer.validated_data["longitude"]
        radius_km = serializer.validated_data["radius"]

        center = GeoPoint(longitude, latitude, srid=4326)
        points = Point.objects.filter(
            location__distance_lte=(center, D(km=radius_km))
        ).select_related("created_by").prefetch_related("messages")

        point_serializer = PointSerializer(points, many=True)
        return Response(point_serializer.data)


class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для работы с сообщениями."""

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related("author", "point", "point__created_by")
        return queryset

    @action(
        detail=False,
        methods=["get"],
        url_path="search",
        serializer_class=MessageSearchSerializer,
    )
    def search(self, request):
        serializer = MessageSearchSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        latitude = serializer.validated_data["latitude"]
        longitude = serializer.validated_data["longitude"]
        radius_km = serializer.validated_data["radius"]

        center = GeoPoint(longitude, latitude, srid=4326)
        messages = Message.objects.filter(
            point__location__distance_lte=(center, D(km=radius_km))
        ).select_related("author", "point", "point__created_by")

        message_serializer = MessageSerializer(messages, many=True)
        return Response(message_serializer.data)
