from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404

# Временные данные
cats_db = [
    {'id': 1, 'slug': 'breakfast', 'name': 'Завтрак'},
    {'id': 2, 'slug': 'dinner', 'name': 'Обед'},
    {'id': 3, 'slug': 'lunch', 'name': 'Ужин'},
    {'id': 4, 'slug': 'desserts', 'name': 'Десерты'},
]

posts_db = [
    {
        'id': 1,
        'title': 'Омлет с овощами',
        'slug': 'omlet-ovoshi',
        'content': 'Простой и быстрый рецепт омлета с помидорами и перцем. Идеально для завтрака.',
        'category': cats_db[0],
        'is_published': True,
    },
    {
        'id': 2,
        'title': 'Паста карбонара',
        'slug': 'pasta-carbonara',
        'content': 'Классическая итальянская паста с беконом и сыром. Подходит для обеда.',
        'category': cats_db[1],
        'is_published': True,
    },
    {
        'id': 3,
        'title': 'Куриный суп',
        'slug': 'kurinii-sup',
        'content': 'Легкий куриный суп с лапшой. Отличный ужин.',
        'category': cats_db[2],
        'is_published': False,
    },
    {
        'id': 4,
        'title': 'Шоколадный брауни',
        'slug': 'shokoladnii-brauni',
        'content': 'Очень шоколадный десерт с хрустящей корочкой и мягкой серединой.',
        'category': cats_db[3],
        'is_published': True,
    },
]

menu = ["О нас", "Контакты", "Помощь"]


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


def index(request):
    data = {
        'title': 'Главная страница рецептов',
        'menu': menu,
        'int': 27,
        'posts': posts_db,
        'cat_selected': 0,
    }
    return render(request, 'home.html', context=data)


def categories_recipes(request, cat_slug):
    category = next((cat for cat in cats_db if cat['slug'] == cat_slug), None)
    if not category:
        raise Http404("Категория не найдена")
    posts = [p for p in posts_db if p['category']['id'] == category['id'] and p['is_published']]
    data = {
        'title': f'Рецепты: {category["name"]}',
        'menu': menu,
        'posts': posts,
        'cat_name': category['name'],
        'cat_selected': category['id'],
    }
    return render(request, 'categories.html', context=data)


def recipe_detail(request, recipe_slug):
    post = next((p for p in posts_db if p['slug'] == recipe_slug), None)
    if not post:
        raise Http404("Рецепт не найден")
    data = {
        'title': post['title'],
        'menu': menu,
        'post': post,
    }
    return render(request, 'recipe_detail.html', context=data)


def recipes_by_portions(request, count):
    data = {
        'title': f'Рецепты на {count} порции',
        'menu': menu,
        'count': count,
    }
    return render(request, 'portion.html', context=data)


def home(request):
    links = [
        ("Главная Recipes", "/Recipes/"),
        ("Категория breakfast", "/Recipes/cats/breakfast/"),
        ("Категория dinner", "/Recipes/cats/dinner/"),
        ("Категория lunch", "/Recipes/cats/lunch/"),
        ("Категория desserts", "/Recipes/cats/desserts/"),
        ("Категория breakfast с GET-параметром (max_calories=300)", "/Recipes/cats/breakfast/?max_calories=300"),
        ("Рецепты на 4 порции", "/Recipes/portion/4/"),
        ("Рецепт pizza", "/Recipes/pizza/"),
        ("Рецепт pasta", "/Recipes/pasta/"),
        ("Рецепт salat", "/Recipes/salat/"),
        ("Несуществующая категория (404)", "/Recipes/cats/aaa/"),
        ("Несуществующий рецепт (404)", "/Recipes/unknown/"),
        ("Главная Users", "/Users/"),
        ("Регистрация Users", "/Users/registration/"),
        ("Профиль Users", "/Users/profile/"),
    ]
    html = "<h1>Ссылки для тестирования SmartPlate</h1><ul>"
    for name, url in links:
        html += f'<li><a href="{url}">{name}</a> — {url}</li>'
    html += "</ul>"
    return HttpResponse(html)