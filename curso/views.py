from django.shortcuts import render, redirect
from curso.models import Curso, Disciplina, Projeto
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User

def custom_logout(request):
    logout(request)
    return redirect('cursos:registro')  # Redireciona para a página de registro após o logout

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('cursos:cursos')
    else:
        form = UserCreationForm()
    return render(request, 'cursos/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('cursos:cursos')  # Redireciona para a página principal após o login
    else:
        form = AuthenticationForm()
    return render(request, 'cursos/login.html', {'form': form})

def password_reset(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            return redirect('cursos:login')  # Redirecionar para a página de login após a redefinição de senha
        except User.DoesNotExist:
            # Tratar o caso em que o nome de usuário não existe
            return render(request, 'cursos/password_reset.html', {'error_message': 'Nome de usuário não encontrado. Por favor, tente novamente.'})
    else:
        return render(request, 'cursos/password_reset.html')

def lista_cursos(request):
    cursos = Curso.objects.all()
    context = {'cursos': cursos}
    return render(request, 'curso/lista_cursos.html', context)

def detalhes_curso(request, curso_nome):
    curso = Curso.objects.get(nome=curso_nome)
    disciplinas = curso.disciplinas.all()
    context = {'curso': curso, 'disciplinas': disciplinas}
    return render(request, 'curso/detalhes_curso.html', context)

def detalhes_disciplina(request, disciplina_nome):
    disciplina = Disciplina.objects.get(nome=disciplina_nome)
    projetos = Projeto.objects.filter(disciplina=disciplina)
    context = {'disciplina': disciplina, 'projetos': projetos}
    return render(request, 'curso/detalhes_disciplina.html', context)

def detalhes_projeto(request, projeto_nome):
    projeto = Projeto.objects.get(nome=projeto_nome)
    context = {'projeto': projeto}
    return render(request, 'curso/detalhes_projeto.html', context)
