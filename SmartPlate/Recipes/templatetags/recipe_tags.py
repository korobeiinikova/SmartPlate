from django import template
from Recipes.models import RecipeCategory, Tag
from django.db.models import Count

register = template.Library()

@register.inclusion_tag('categories_menu.html')
def show_categories(cat_selected=0):
    cats = RecipeCategory.objects.all()
    return {'cats': cats, 'cat_selected': cat_selected}

@register.inclusion_tag('tags_menu.html')
def show_all_tags():
    tags = Tag.objects.annotate(total=Count('recipes')).filter(total__gt=0)
    return {'tags': tags}