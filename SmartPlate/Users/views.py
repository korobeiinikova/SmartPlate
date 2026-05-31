from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views.generic import UpdateView
from .forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm


def index(request):
    return render(request, 'users/index.html')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        return reverse_lazy('Recipes:home')


def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password']
            )

            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('Recipes:home'))
    else:
        form = LoginUserForm()

    return render(request, 'users/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('Users:login'))


def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return HttpResponseRedirect(reverse('Users:login'))
    else:
        form = RegisterUserForm()

    return render(request, 'users/registration.html', {'form': form})


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('Users:login')
    extra_context = {'title': 'Регистрация'}


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('Users:profile')
    extra_context = {'title': 'Профиль пользователя'}

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'users/password_change_form.html'
    success_url = reverse_lazy('Users:password_change_done')
    extra_context = {'title': 'Смена пароля'}
