from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from .forms import RegistrationForm, LoginForm


class UserLoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/accounts/home')

        form = LoginForm()
        context = {'form': form}
        return render(request, 'login.html', context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')

        context = {'form': form}
        return render(request, 'login.html', context)


class UserRegisterView(View):
    def get(self, request):
        form = RegistrationForm()
        context = {'form': form}
        return render(request, 'register.html', context)

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.birth_date = form.cleaned_data['birth_date']
            user.birth_hour = form.cleaned_data['birth_hour']
            user.birth_place = form.cleaned_data['birth_place']
            user.save()

            messages.success(request, f'Account created for {user.username}!')
            return redirect('login')
        else:
            for key, error in form.errors.items():
                messages.error(request, error)
                print(key, error)
            context = {'form': form}
            return render(request, 'register.html', context)


class HomeView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'home.html')


class UserLogoutView(View):
    @method_decorator(login_required)
    def get(self, request):
        logout(request)
        return redirect('index')



