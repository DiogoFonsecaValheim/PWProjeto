from django.shortcuts import render, redirect, get_object_or_404
from .models import Curso, Disciplina, Projeto, Area_Cientifica
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .forms import ProjetoForm, DisciplinaForm, CursoForm

def custom_logout(request):
    logout(request)
    return redirect('curso:registro')  # Redireciona para a página de registro após o logout

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('curso:lista_cursos')
    else:
        form = UserCreationForm()
    return render(request, 'curso/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('cursos:lista_cursos')  # Redireciona para a página principal após o login
    else:
        form = AuthenticationForm()
    return render(request, 'curso/login.html', {'form': form})

def password_reset(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            return redirect('curso:login')  # Redirecionar para a página de login após a redefinição de senha
        except User.DoesNotExist:
            # Tratar o caso em que o nome de usuário não existe
            return render(request, 'curso/password_reset.html', {'error_message': 'Nome de usuário não encontrado. Por favor, tente novamente.'})
    else:
        return render(request, 'curso/password_reset.html')


def lista_cursos(request):
    cursos = Curso.objects.all()
    context = {'cursos': cursos}
    return render(request, 'curso/lista_cursos.html', context)

def detalhes_curso(request, curso_nome):
    curso = get_object_or_404(Curso, nome=curso_nome)

    context = {
        'curso': curso,
        'disciplinas': curso.disciplinas.all(),  # Certifique-se de que está carregando as disciplinas do curso
    }
    return render(request, 'curso/detalhes_curso.html', context)

def detalhes_disciplina(request, disciplina_nome):
    disciplina = Disciplina.objects.get(nome=disciplina_nome)
    projetos = Projeto.objects.filter(disciplina=disciplina)

    context = {
        'disciplina': disciplina,
        'projetos': projetos,
    }
    return render(request, 'curso/detalhes_disciplina.html', context)

def adicionar_projeto(request, disciplina_nome):
    disciplina = Disciplina.objects.get(nome=disciplina_nome)

    if request.method == 'POST':
        form = ProjetoForm(request.POST, request.FILES)
        if form.is_valid():
            projeto = form.save(commit=False)
            projeto.disciplina = disciplina
            projeto.save()
            return redirect('cursos:detalhes_disciplina', disciplina_nome=disciplina_nome)
    else:
        form = ProjetoForm()

    context = {
        'disciplina': disciplina,
        'form': form,
    }
    return render(request, 'curso/adicionar_projeto.html', context)

def detalhes_projeto(request, projeto_nome):
    projeto = Projeto.objects.get(nome=projeto_nome)
    context = {'projeto': projeto}
    return render(request, 'curso/detalhes_projeto.html', context)

def editar_disciplina(request, disciplina_nome):
    disciplina = Disciplina.objects.get(nome=disciplina_nome)

    if request.method == 'POST':
        form = DisciplinaForm(request.POST, instance=disciplina)
        if form.is_valid():
            form.save()
            return redirect('cursos:detalhes_disciplina', disciplina_nome=disciplina.nome)
    else:
        form = DisciplinaForm(instance=disciplina)

    context = {
        'disciplina': disciplina,
        'form': form,
    }
    return render(request, 'curso/editar_disciplina.html', context)

def remover_disciplina(request, disciplina_nome):
    disciplina = Disciplina.objects.get(nome=disciplina_nome)

    if request.method == 'POST':
        disciplina.delete()
        return redirect('cursos:lista_cursos')

    context = {
        'disciplina': disciplina,
    }
    return render(request, 'curso/remover_disciplina.html', context)

def editar_projeto(request, projeto_nome):
    projeto = get_object_or_404(Projeto, nome=projeto_nome)

    if request.method == 'POST':
        form = ProjetoForm(request.POST, instance=projeto)
        if form.is_valid():
            form.save()
            return redirect('cursos:detalhes_projeto', projeto_nome=projeto.nome)
    else:
        form = ProjetoForm(instance=projeto)

    context = {
        'projeto': projeto,
        'form': form,
    }
    return render(request, 'curso/editar_projeto.html', context)

def remover_projeto(request, projeto_nome):
    projeto = get_object_or_404(Projeto, nome=projeto_nome)

    if request.method == 'POST':
        projeto.delete()
        return redirect('cursos:detalhes_disciplina', disciplina_nome=projeto.disciplina.nome)

    context = {
        'projeto': projeto,
    }
    return render(request, 'curso/remover_projeto.html', context)


def adicionar_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cursos:lista_cursos')
    else:
        dados_padrao = {
            'apresentacao': 'Apresentação padrão',
            'objetivos': 'Objetivos padrão',
            'competencias': 'Competências padrão',
        }
        form = CursoForm(initial=dados_padrao)

    context = {
        'form': form,
    }
    return render(request, 'curso/adicionar_curso.html', context)

def editar_curso(request, curso_nome):
    curso = Curso.objects.get(nome=curso_nome)

    if request.method == 'POST':
        # Se o formulário de edição for submetido, processá-lo
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            return redirect('cursos:lista_cursos')
    else:
        # Se for um GET request, preencher o formulário com os dados do curso existente
        form = CursoForm(instance=curso)

    context = {
        'curso': curso,
        'form': form,
    }
    return render(request, 'curso/editar_curso.html', context)

def remover_curso(request, curso_nome):
    curso = Curso.objects.get(nome=curso_nome)

    if request.method == 'POST':
        # Se a confirmação de remoção for submetida, remover o curso
        curso.delete()
        return redirect('cursos:lista_cursos')

    context = {
        'curso': curso,
    }
    return render(request, 'curso/remover_curso.html', context)


def adicionar_disciplina(request, curso_nome):
    curso = get_object_or_404(Curso, nome=curso_nome)
    if request.method == 'POST':
        form = DisciplinaForm(request.POST)
        if form.is_valid():
            disciplina = form.save()
            curso.disciplinas.add(disciplina)  # Adicionando a disciplina ao curso
            return redirect('cursos:detalhes_curso', curso_nome=curso.nome)
    else:
        form = DisciplinaForm()
    return render(request, 'curso/adicionar_disciplina.html', {'form': form, 'curso': curso})