from django.urls import path, register_converter
from Recipes import views, converters

register_converter(converters.PositiveIntConverter, "posint")
app_name = 'Recipes'

urlpatterns = [
    path('', views.index, name='home'),
    # path('cats/<slug:cat_slug>/', views.categories_recipes, name='cats'),  # отключено для ЛР7
    path('portion/<posint:count>/', views.recipes_by_portions, name='recipes_by_portions'),
    path('<slug:recipe_slug>/', views.recipe_detail, name='recipe_detail'),
]