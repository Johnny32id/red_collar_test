"""
Админ-панель для моделей точек и сообщений.
"""
from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from .models import Point, Message


@admin.register(Point)
class PointAdmin(GISModelAdmin):
    list_display = ["name", "created_by", "created_at", "location"]
    list_filter = ["created_at", "created_by"]
    search_fields = ["name", "description"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["point", "author", "created_at", "text_preview"]
    list_filter = ["created_at", "author"]
    search_fields = ["text", "point__name"]
    readonly_fields = ["created_at", "updated_at"]

    def text_preview(self, obj: Message) -> str:
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text

    text_preview.short_description = "Превью текста"
