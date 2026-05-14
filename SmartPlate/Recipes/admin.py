from django.contrib import admin, messages
from .models import Recipe, RecipeCategory, Tag, Product, RecipeIngredient, RecipeDetail
from django.utils.html import mark_safe
# Register your models here.
admin.site.register(Tag)
admin.site.register(Product)
admin.site.register(RecipeIngredient)
admin.site.register(RecipeDetail)


class CalorieFilter(admin.SimpleListFilter):
    title = 'Калорийность'
    parameter_name = 'calories_range'

    def lookups(self, request, model_admin):
        return [
            ('low', 'Низкая (<200 ккал)'),
            ('medium', 'Средняя (200-500 ккал)'),
            ('high', 'Высокая (>500 ккал)'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'low':
            return queryset.filter(calories__lt=200)
        if self.value() == 'medium':
            return queryset.filter(calories__gte=200, calories__lte=500)
        if self.value() == 'high':
            return queryset.filter(calories__gt=500)
        return queryset


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    @admin.display(description="Изображение")
    def preview_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="100" />')
        return "Нет фото"
    list_display = ('id', 'title', 'category', 'is_published', 'time_create', 'brief_info', 'calories_status', 'preview_photo')
    list_display_links = ('id', 'title')
    ordering = ['-time_create', 'title']
    list_per_page = 5
    actions = ['set_published', 'set_draft']
    search_fields = ['title', 'description', 'instructions', 'category__name']
    list_filter = ['category', 'is_published', 'tags', CalorieFilter]
    fields = ('title', 'slug', 'category', 'description', 'instructions',
              'calories', 'proteins', 'fats', 'carbs', 'tags', 'is_published', 'photo', 'preview_photo')
    readonly_fields = ('slug', 'preview_photo')
    filter_horizontal = ('tags',)

    @admin.display(description="Краткое описание")
    def brief_info(self, recipe: Recipe):
        return f"Описание: {len(recipe.description)} симв."

    @admin.display(description="Калорийность")
    def calories_status(self, recipe: Recipe):
        if recipe.calories > 500:
            return "Высокая"
        elif recipe.calories > 200:
            return "Средняя"
        else:
            return "Низкая"

    @admin.action(description="Опубликовать выбранные рецепты")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=True)
        self.message_user(request, f"Опубликовано {count} рецептов.")

    @admin.action(description="Снять с публикации выбранные рецепты")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=False)  # вместо Recipe.Status.DRAFT
        self.message_user(request, f"{count} рецептов сняты с публикации.", messages.WARNING)


@admin.register(RecipeCategory)
class RecipeCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
