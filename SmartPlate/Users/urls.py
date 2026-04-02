from django.urls import path, register_converter, re_path
from Users import views

app_name = 'Users'

urlpatterns = [
     path('', views.index, name='home'),
     path('registration/', views.registration, name='registration'),
     path('profile/', views.profile, name='profile'),
]
