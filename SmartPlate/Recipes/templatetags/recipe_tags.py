"""Теги шаблонов для вывода категорий и тегов рецептов."""

from django import template
from django.db.models import Count

from Recipes.models import RecipeCategory, Tag

register = template.Library()


@register.inclusion_tag('categories_menu.html')
def show_categories(cat_selected=0):
    """Возвращает список категорий и текущую выбранную категорию."""
    categories = RecipeCategory.objects.all()
    return {
        'cats': categories,
        'cat_selected': cat_selected,
    }


@register.inclusion_tag('tags_menu.html')
def show_all_tags():
    """Выводит только теги, связанные хотя бы с одним рецептом."""
    tags = Tag.objects.annotate(
        total=Count('recipes'),
    ).filter(total__gt=0)
    return {'tags': tags}
