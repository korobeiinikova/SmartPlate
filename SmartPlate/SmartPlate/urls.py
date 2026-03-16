from django.contrib import admin
from django.urls import path, include
from Recipes.views import page_not_found, home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Recipes/', include('Recipes.urls')),
    path('Users/', include('Users.urls')),
    path('', home, name='home'),
]

handler404 = page_not_found
