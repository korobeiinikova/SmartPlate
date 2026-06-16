"""Настройки отображения моделей Recipes в панели администратора."""

from django.contrib import admin, messages
from django.utils.html import format_html

from .models import (
    Favorite,
    Product,
    Recipe,
    RecipeCategory,
    RecipeComment,
    RecipeDetail,
    RecipeIngredient,
    Tag,
)


# Простые справочники не требуют отдельного класса ModelAdmin.
admin.site.register(Tag)
admin.site.register(Product)
admin.site.register(RecipeIngredient)
admin.site.register(RecipeDetail)
admin.site.register(RecipeComment)
admin.site.register(Favorite)


class CalorieFilter(admin.SimpleListFilter):
    """Фильтр списка рецептов по диапазону калорийности."""

    title = 'Калорийность'
    parameter_name = 'calories_range'

    def lookups(self, request, _model_admin):
        return [
            ('low', 'Низкая (<200 ккал)'),
            ('medium', 'Средняя (200-500 ккал)'),
            ('high', 'Высокая (>500 ккал)'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'low':
            return queryset.filter(calories__lt=200)
        if self.value() == 'medium':
            return queryset.filter(calories__range=(200, 500))
        if self.value() == 'high':
            return queryset.filter(calories__gt=500)
        return queryset


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Расширенное управление рецептами в админке."""

    list_display = (
        'id',
        'title',
        'category',
        'is_published',
        'time_create',
        'brief_info',
        'calories_status',
        'preview_photo',
    )
    list_display_links = ('id', 'title')
    ordering = ('-time_create', 'title')
    list_per_page = 5
    actions = ('set_published', 'set_draft')
    search_fields = ('title', 'description', 'instructions', 'category__name')
    list_filter = ('category', 'is_published', 'tags', CalorieFilter)
    fields = (
        'title',
        'slug',
        'category',
        'description',
        'instructions',
        'calories',
        'proteins',
        'fats',
        'carbs',
        'tags',
        'is_published',
        'photo',
        'preview_photo',
    )
    readonly_fields = ('slug', 'preview_photo')
    filter_horizontal = ('tags',)

    @admin.display(description='Изображение')
    def preview_photo(self, recipe):
        """Показывает небольшое превью загруженной фотографии."""
        if recipe.photo:
            return format_html(
                '<img src="{}" width="100" alt="Превью">',
                recipe.photo.url,
            )
        return 'Нет фото'

    @admin.display(description='Краткое описание')
    def brief_info(self, recipe):
        return f'Описание: {len(recipe.description)} симв.'

    @admin.display(description='Калорийность')
    def calories_status(self, recipe):
        if recipe.calories > 500:
            return 'Высокая'
        if recipe.calories > 200:
            return 'Средняя'
        return 'Низкая'

    @admin.action(description='Опубликовать выбранные рецепты')
    def set_published(self, request, queryset):
        updated_count = queryset.update(is_published=True)
        self.message_user(
            request,
            f'Опубликовано рецептов: {updated_count}.',
        )

    @admin.action(description='Снять выбранные рецепты с публикации')
    def set_draft(self, request, queryset):
        updated_count = queryset.update(is_published=False)
        self.message_user(
            request,
            f'Снято с публикации рецептов: {updated_count}.',
            messages.WARNING,
        )


@admin.register(RecipeCategory)
class RecipeCategoryAdmin(admin.ModelAdmin):
    """Отображение категорий рецептов."""

    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
