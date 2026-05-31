from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from Recipes.views import page_not_found
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('Recipes/', include('Recipes.urls')),
    path('users/', include('Users.urls', namespace='Users')),
    path('', RedirectView.as_view(url='/Recipes/'), name='home'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = page_not_found

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Управление рецептами"
