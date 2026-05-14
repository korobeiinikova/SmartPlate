from django.urls import path, register_converter
from Recipes import views, converters

register_converter(converters.PositiveIntConverter, "posint")
app_name = 'Recipes'

urlpatterns = [
    path('', views.index, name='home'),
    path('category/<slug:cat_slug>/', views.show_category, name='category'),
    path('tag/<slug:tag_slug>/', views.show_tag_postlist, name='tag'),
    path('portion/<posint:count>/', views.recipes_by_portions, name='recipes_by_portions'),
    path('add_model/', views.add_recipe_model, name='add_recipe_model'),
    path('addpage/', views.addpage, name='addpage'),
    path('upload/', views.upload_file, name='upload_file'),
    path('<slug:recipe_slug>/', views.recipe_detail, name='recipe_detail'),

]
