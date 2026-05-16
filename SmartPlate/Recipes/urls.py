from django.urls import path, register_converter
from Recipes import views, converters

register_converter(converters.PositiveIntConverter, "posint")
app_name = 'Recipes'

urlpatterns = [
    path('', views.RecipesHome.as_view(), name='home'),
    path('addpage/', views.AddPageCreateView.as_view(), name='addpage'),
    path('about/', views.about, name='about'),
    path('category/<slug:cat_slug>/', views.RecipesCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.show_tag_postlist, name='tag'),
    path('portion/<posint:count>/', views.recipes_by_portions, name='recipes_by_portions'),
    path('add_model/', views.add_recipe_model, name='add_recipe_model'),
    path('upload/', views.upload_file, name='upload_file'),
    path('edit/<int:pk>/', views.UpdatePage.as_view(), name='edit_page'),
    path('delete/<int:pk>/', views.DeleteRecipe.as_view(), name='delete_recipe'),
    path('<slug:recipe_slug>/', views.RecipeDetail.as_view(), name='recipe_detail'),
]
