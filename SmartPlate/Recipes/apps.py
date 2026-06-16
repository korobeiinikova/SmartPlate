"""Настройка Django-приложения Recipes."""

from django.apps import AppConfig


class RecipesConfig(AppConfig):
    """Конфигурация приложения с рецептами."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Recipes'
    verbose_name = 'Рецепты и кулинария'
