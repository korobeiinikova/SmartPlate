"""Настройки пользовательской модели в панели администратора."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Добавляет фотографию и дату рождения к стандартной форме пользователя."""

    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительные поля', {
            'fields': ('photo', 'date_birth'),
        }),
    )
