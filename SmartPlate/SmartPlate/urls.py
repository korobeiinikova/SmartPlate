"""Корневые маршруты проекта SmartPlate."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from Recipes.views import page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Recipes/', include('Recipes.urls')),
    path('users/', include('Users.urls', namespace='Users')),

    # Корень сайта перенаправляет пользователя в каталог рецептов.
    path('', RedirectView.as_view(url='/Recipes/'), name='home'),
]

# Во время разработки Django самостоятельно раздаёт загруженные файлы.
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

handler404 = page_not_found

# Заголовки стандартной панели администратора.
admin.site.site_header = 'Панель администрирования'
admin.site.index_title = 'Управление рецептами'
