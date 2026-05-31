from django.urls import path
from . import views
from django.contrib.auth.views import (
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

app_name = 'Users'

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('profile/', views.ProfileUser.as_view(), name='profile'),
    path(
        'password-change/',
        PasswordChangeView.as_view(
            template_name='users/password_change_form.html',
            success_url='/users/password-change/done/'
        ),
        name='password_change'
    ),
    path(
        'password-change/done/',
        PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html'
        ),
        name='password_change_done'
    ),
    path(
        'password-reset/',
        PasswordResetView.as_view(
            template_name='users/password_reset_form.html',
            email_template_name='users/password_reset_email.html',
            success_url='/users/password-reset/done/'
        ),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html',
            success_url='/users/password-reset/complete/'
        ),
        name='password_reset_confirm'
    ),
    path(
        'password-reset/complete/',
        PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]
