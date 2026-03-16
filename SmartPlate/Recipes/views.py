from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.template.loader import render_to_string

#####################
# Create your views here.
def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

menu = ["1", "2", "3"]

def index(request):
    data = {
        'title':'gлавная страница!',
        'menu':menu,
        'int':27,
    }

    return render(request, 'home.html', context=data)


def categories_recipes(request, cat_slug):
    categories = ['breakfast', 'dinner', 'lunch', 'desserts']
    if cat_slug not in categories:
        raise Http404("Категория не найдена")

    text = f"<h1>Рецепты по категориям</h1><p >slug: {cat_slug}</p>"
    if request.method == 'GET':
        max_calories = request.GET.get('max_calories')
        if max_calories:
            text += f", фильтр по калориям ≤ {max_calories}"
    if request.method == 'POST':
        print(request.POST)
    return HttpResponse(text)


def recipe_detail(request, recipe_slug):
    recipes = ['pizza', 'pasta', 'salat']
    if recipe_slug not in recipes:
        raise Http404("Категория не найдена")

    return HttpResponse("Recipe.")


def recipes_by_portions(request, count):
    return HttpResponse(f"Рецепты на {count} порции")


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
