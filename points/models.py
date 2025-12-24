"""
Модели для работы с географическими точками и сообщениями.
"""
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Point(models.Model):
    """Модель географической точки на карте."""

    location = models.PointField(
        srid=4326,
        verbose_name="Координаты",
        help_text="Географические координаты точки (долгота, широта)",
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Название",
        help_text="Название точки",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание",
        help_text="Описание точки",
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_points",
        verbose_name="Создатель",
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Дата создания",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления",
    )

    class Meta:
        verbose_name = "Точка"
        verbose_name_plural = "Точки"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.location.y}, {self.location.x})"

    @property
    def latitude(self) -> float:
        return self.location.y

    @property
    def longitude(self) -> float:
        return self.location.x


class Message(models.Model):
    """Модель сообщения к географической точке."""

    point = models.ForeignKey(
        Point,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="Точка",
    )
    text = models.TextField(
        verbose_name="Текст сообщения",
        help_text="Содержимое сообщения",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="Автор",
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Дата создания",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления",
    )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["point"]),
        ]

    def __str__(self) -> str:
        return f"Сообщение от {self.author.username} к точке {self.point.name}"
