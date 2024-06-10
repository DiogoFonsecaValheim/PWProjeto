from django.shortcuts import render,redirect
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login

def home(request):
    personal_info = {
        'name': 'Diogo Fonseca',
        'email': 'diogommfonseca@gmail.com',
        'phone': '+351 123 456 789',
        'bio': 'Aluno do 2o ano de Engenharia Informática na Universidade Lusófona de Humanidades e Tecnologias.'
    }
    return render(request, 'portfolio/home.html', {'personal_info': personal_info})

def projects(request):
    projects = [
        {'title': 'Bandas', 'description': 'Site onde guarda informaçoes sobre varias bandas', 'url': 'https://a22204579.pythonanywhere.com/bandas'},
        {'title': 'Artigos', 'description': 'Site onde guarda informaçoes sobre artigos', 'url': 'https://a22204579.pythonanywhere.com/artigos'},
        {'title': 'Cursos', 'description': 'Site onde guarda informaçoes sobre cursos', 'url': 'https://a22204579.pythonanywhere.com/cursos'},
        {'title': 'Metereologia', 'description': 'Site de metereologia', 'url': 'https://a22204579.pythonanywhere.com/meteo'},
    ]
    return render(request, 'portfolio/projects.html', {'projects': projects})

def technologies(request):
    return render(request, 'portfolio/technologies.html')

def custom_logout(request):
    logout(request)
    return redirect('portfolio:registro')  # Redireciona para a página de registro após o logout


def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('artigos:artigos')
    else:
        form = UserCreationForm()
    return render(request, 'artigos/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('portfolio:home')  # Redireciona para a página principal após o login
    else:
        form = AuthenticationForm()
    return render(request, 'portfolio/login.html', {'form': form})


def password_reset(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            return redirect('portfolio:login')  # Redirecionar para a página de login após a redefinição de senha
        except User.DoesNotExist:
            # Tratar o caso em que o nome de usuário não existe
            return render(request, 'portfolio/password_reset.html', {'error_message': 'Nome de usuário não encontrado. Por favor, tente novamente.'})
    else:
        return render(request, 'portfolio/password_reset.html')
