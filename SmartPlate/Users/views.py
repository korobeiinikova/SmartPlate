from django.http import HttpResponse
from django.shortcuts import render, redirect


def index(request):
    return HttpResponse("Страница приложения users.")


def registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        return redirect('profile')
    return HttpResponse("Страница регистрации.")


def profile(request):
    return HttpResponse("<h1>Личный кабинет пользователя</h1>")
