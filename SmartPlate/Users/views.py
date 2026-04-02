from django.shortcuts import render, redirect
from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')

def registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        return redirect('Users:profile')
    return render(request, 'registration.html')

def profile(request):
    return render(request, 'profile.html')
