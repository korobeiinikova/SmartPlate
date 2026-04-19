from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from Recipes.views import page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Recipes/', include('Recipes.urls')),
    path('Users/', include('Users.urls')),
    path('', RedirectView.as_view(url='/Recipes/'), name='home'),
]

handler404 = page_not_found

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Управление рецептами"
