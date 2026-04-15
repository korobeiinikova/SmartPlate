from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from .models import Recipe, RecipeCategory, Tag


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


def index(request):
    posts = Recipe.published.all()
    data = {
        'title': 'Главная страница рецептов',
        'posts': posts,
        'cat_selected': 0,
    }
    return render(request, 'home.html', context=data)


def show_category(request, cat_slug):
    category = get_object_or_404(RecipeCategory, slug=cat_slug)
    posts = category.recipes.filter(is_published=Recipe.Status.PUBLISHED)
    data = {
        'title': f'Категория: {category.name}',
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, 'home.html', context=data)


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = tag.recipes.filter(is_published=Recipe.Status.PUBLISHED)
    data = {
        'title': f'Тег: {tag.name}',
        'posts': posts,
        'tag_selected': tag,
    }
    return render(request, 'home.html', context=data)


def recipe_detail(request, recipe_slug):
    post = get_object_or_404(Recipe, slug=recipe_slug)
    data = {
        'title': post.title,
        'post': post,
    }
    return render(request, 'recipe_detail.html', context=data)


def recipes_by_portions(request, count):
    data = {
        'title': f'Рецепты на {count} порции',
        'count': count,
    }
    return render(request, 'portion.html', context=data)


def home(request):
    # Страница для тестирования (не используется в основном сайте)
    links = [
        ("Главная Recipes", "/Recipes/"),
        ("Категория breakfast", "/Recipes/cats/breakfast/"),
        ("Категория dinner", "/Recipes/cats/dinner/"),
        ("Категория lunch", "/Recipes/cats/lunch/"),
        ("Категория desserts", "/Recipes/cats/desserts/"),
        ("Категория breakfast с GET-параметром (max_calories=300)", "/Recipes/cats/breakfast/?max_calories=300"),
        ("Рецепты на 4 порции", "/Recipes/portion/4/"),
        ("Главная Users", "/Users/"),
        ("Регистрация Users", "/Users/registration/"),
        ("Профиль Users", "/Users/profile/"),
    ]
    html = "<h1>Ссылки для тестирования SmartPlate</h1><ul>"
    for name, url in links:
        html += f'<li><a href="{url}">{name}</a> — {url}</li>'
    html += "</ul>"
    return HttpResponse(html)
