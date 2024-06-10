from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import BandaForm, CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Banda, Album, Musicas
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import AlbumForm, MusicaForm
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import logout

def custom_logout(request):
    logout(request)
    return redirect('bandas:registro')  # Redireciona para a página de registro após o logout

@login_required
def banda_adicionar(request):
    if request.method == 'POST':
        form = BandaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bandas:bandas')
    else:
        form = BandaForm()
    return render(request, 'bandas/banda_adicionar.html', {'form': form})

@login_required
def banda_editar(request, pk):
    banda = get_object_or_404(Banda, pk=pk)
    if request.method == 'POST':
        form = BandaForm(request.POST, instance=banda)
        if form.is_valid():
            form.save()
            return redirect('bandas:banda', banda_nome=banda.nome)
    else:
        form = BandaForm(instance=banda)
    return render(request, 'bandas/banda_editar.html', {'form': form})

@login_required
def banda_remover(request, pk):
    banda = get_object_or_404(Banda, pk=pk)
    banda.delete()
    return redirect('bandas:bandas')

@login_required
def musica_adicionar(request, banda_nome, album_titulo):
    if request.method == 'POST':
        form = MusicaForm(request.POST)
        if form.is_valid():
            musica = form.save(commit=False)
            album = Album.objects.get(titulo=album_titulo)
            musica.album = album
            musica.save()
            return redirect('bandas:album', banda_nome=banda_nome, album_titulo=album_titulo)
    else:
        form = MusicaForm()

    context = {'form': form}
    return render(request, 'bandas/musica_adicionar.html', context)

@login_required
def musica_editar(request, pk):
    musica = get_object_or_404(Musicas, pk=pk)
    if request.method == 'POST':
        form = MusicaForm(request.POST, instance=musica)
        if form.is_valid():
            form.save()
            return redirect('bandas:banda', banda_nome=musica.album.banda.nome)
    else:
        form = MusicaForm(instance=musica)
    return render(request, 'bandas/musica_editar.html', {'form': form})


@login_required
def musica_remover(request, pk):
    musica = get_object_or_404(Musicas, pk=pk)
    musica.delete()
    return redirect('bandas:banda', banda_nome=musica.album.banda.nome)


@login_required
def album_adicionar(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('bandas:bandas')  # Redireciona para a página principal após adicionar o álbum
    else:
        form = AlbumForm()
    return render(request, 'bandas/album_adicionar.html', {'form': form})

@login_required
def album_editar(request, pk):
    album = get_object_or_404(Album, pk=pk)
    if request.method == 'POST':
        form = AlbumForm(request.POST, instance=album)
        if form.is_valid():
            form.save()
            return redirect('bandas:banda', banda_nome=album.banda.nome)
    else:
        form = AlbumForm(instance=album)
    return render(request, 'bandas/album_editar.html', {'form': form})

@login_required
def album_remover(request, pk):
    album = get_object_or_404(Album, pk=pk)
    banda_nome = album.banda.nome
    album.delete()
    return redirect('bandas:banda', banda_nome=banda_nome)



# Adicione as views de registro e login
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
            return redirect('bandas:bandas')  # Redireciona para a página principal após o login
    else:
        form = AuthenticationForm()
    return render(request, 'bandas/login.html', {'form': form})


def password_reset(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            return redirect('bandas:login')  # Redirecionar para a página de login após a redefinição de senha
        except User.DoesNotExist:
            # Tratar o caso em que o nome de usuário não existe
            return render(request, 'bandas/password_reset.html', {'error_message': 'Nome de usuário não encontrado. Por favor, tente novamente.'})
    else:
        return render(request, 'bandas/password_reset.html')

# Modifique a view de criação/edição de bandas para requerer login
def banda_form_view(request):
    if not request.user.is_authenticated:
        return redirect('bandas:login')  # Redireciona para a página de login se o usuário não estiver autenticado

    if request.method == 'POST':
        form = BandaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bandas:bandas')
    else:
        form = BandaForm()
    return render(request, 'banda_form.html', {'form': form})


def bandas_view(request):
    bandas = Banda.objects.all()
    context = {
        'bandas': bandas,
    }
    return render(request, 'bandas/bandas.html', context)

def banda_view(request, banda_nome):
    if request.method == 'GET' and banda_nome == 'adicionar':
        # Se a solicitação for GET e o nome da banda for 'adicionar', renderize a página para adicionar uma nova banda
        form = BandaForm()
        return render(request, 'bandas/banda_adicionar.html', {'form': form})
    elif request.method == 'POST':
        # Se a solicitação for POST, processe os dados do formulário para adicionar uma nova banda
        form = BandaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bandas:bandas')  # Redireciona para a página principal após adicionar a banda
        else:
            # Se o formulário não for válido, renderize a página de adicionar banda novamente com os erros
            return render(request, 'bandas/banda_adicionar.html', {'form': form})
    else:
        # Caso contrário, continue com a lógica existente para exibir detalhes da banda
        try:
            banda_nome = banda_nome.replace('-', ' ').title()
            banda = Banda.objects.get(nome=banda_nome)
            albuns = Album.objects.filter(banda=banda)
            context = {
                'banda': banda,
                'albuns': albuns,
            }
            return render(request, 'bandas/banda.html', context)
        except Banda.DoesNotExist:
            raise Http404("A banda não existe")



def album_view(request, banda_nome, album_titulo):
    try:
        banda_nome = banda_nome.replace('-', ' ').title()
        banda = Banda.objects.get(nome=banda_nome)
        album = Album.objects.get(banda=banda, titulo=album_titulo)
        musicas = Musicas.objects.filter(album=album)
    except (Banda.DoesNotExist, Album.DoesNotExist):
        raise Http404("A banda ou o álbum não existe")

    context = {
        'banda': banda,
        'album': album,
        'musicas': musicas,
        'banda_nome': banda_nome,  # Adicionando a variável banda_nome ao contexto
    }
    return render(request, 'bandas/album.html', context)





def musica_view(request, musica_titulo):
    try:
        musica = Musicas.objects.get(titulo=musica_titulo)
        album = musica.album
    except Musicas.DoesNotExist:
        raise Http404("A música não existe")

    context = {
        'musica': musica,
        'album': album,
    }

    return render(request, 'bandas/musica.html', context)

