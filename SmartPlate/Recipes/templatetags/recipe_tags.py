from django import template

register = template.Library()

# Простой тег – возвращает список категорий
@register.simple_tag
def get_categories():
    categories = [
        {'id': 1, 'slug': 'breakfast', 'name': 'Завтрак'},
        {'id': 2, 'slug': 'dinner', 'name': 'Обед'},
        {'id': 3, 'slug': 'lunch', 'name': 'Ужин'},
        {'id': 4, 'slug': 'desserts', 'name': 'Десерты'},
    ]
    return categories

# Inclusion-тег – выводит меню категорий с подсветкой выбранной
@register.inclusion_tag('categories_menu.html')
def show_categories(cat_selected=0):
    categories = [
        {'id': 1, 'slug': 'breakfast', 'name': 'Завтрак'},
        {'id': 2, 'slug': 'dinner', 'name': 'Обед'},
        {'id': 3, 'slug': 'lunch', 'name': 'Ужин'},
        {'id': 4, 'slug': 'desserts', 'name': 'Десерты'},
    ]
    return {'categories': categories, 'cat_selected': cat_selected}