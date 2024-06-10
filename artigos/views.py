from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comen, Rating
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .forms import ArtigoForm, ComenForm, RatingForm
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.http import HttpResponseForbidden


def remover_rating(request, rating_id):
    rating = get_object_or_404(Rating, pk=rating_id)
    artigo_id = rating.post.pk
    rating.delete()
    return redirect('artigos:gerir_ratings', artigo_id=artigo_id)

def editar_rating(request, rating_id):
    rating = get_object_or_404(Rating, pk=rating_id)

    if request.method == 'POST':
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
            form.save()
            return redirect('artigos:gerir_ratings', artigo_id=rating.post.pk)
    else:
        form = RatingForm(instance=rating)

    context = {'form': form, 'rating': rating}
    return render(request, 'artigos/editar_rating.html', context)

def gerir_ratings(request, artigo_id):
    artigo = get_object_or_404(Post, pk=artigo_id)
    ratings = Rating.objects.filter(post=artigo)
    context = {'artigo': artigo, 'ratings': ratings}
    return render(request, 'artigos/gerir_ratings.html', context)

@login_required
def adicionar_rating(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if request.method == 'POST':
        novo_rating = int(request.POST.get('novo_rating'))

        # Verifica se já existe um rating para este usuário e este post
        rating_existente = Rating.objects.filter(post=post, user=user).first()

        if rating_existente:
            # Se existe, atualiza o valor do rating
            rating_existente.valor = novo_rating
            rating_existente.save()
        else:
            # Se não existe, cria um novo rating
            novo_rating = Rating.objects.create(post=post, user=user, valor=novo_rating)

        return redirect('artigos:artigos')
    else:
        # Adicione este contexto para passar o post para o template
        return render(request, 'artigos/adicionar_rating.html', {'post': post})

def remover_comentario(request, comentario_texto):
    comentario = get_object_or_404(Comen, titulo=comentario_texto)
    comentario.delete()
    return redirect('artigos:artigos')


def editar_comentario(request, comentario_texto):
    # Recuperar o comentário com base no texto fornecido
    comentario = get_object_or_404(Comen, titulo=comentario_texto)

    # Se houver uma solicitação POST, isso significa que o comentário está sendo editado
    if request.method == 'POST':
        # Atualizar os dados do comentário com base nos dados enviados no formulário
        comentario.nome = request.POST.get('nome')
        comentario.titulo = request.POST.get('titulo')
        # Salvar as alterações
        comentario.save()
        # Redirecionar de volta para a página de visualização de comentários
        return redirect('artigos:visualizar_comentarios', post_id=comentario.post.pk)

    context = {'comentario': comentario}
    return render(request, 'artigos/editar_comentario.html', context)

def visualizar_comentarios(request, post_id):
    post = Post.objects.get(pk=post_id)
    comentarios = Comen.objects.filter(post=post)

    context = {'post': post, 'comentarios': comentarios}
    return render(request, 'artigos/visualizar_comentarios.html', context)

def adicionar_comentario(request, post_id):
    if request.method == 'POST':
        form = ComenForm(request.POST)
        if form.is_valid():
            # Salvar o comentário associado ao post com o ID post_id
            post = Post.objects.get(id=post_id)
            comentario = form.save(commit=False)
            comentario.post = post
            comentario.save()
            return redirect('artigos:artigos')  # Redirecionar para a página de artigos após adicionar o comentário
    else:
        form = ComenForm()

    # Lidar com solicitações GET
    return render(request, 'artigos/adicionar_comentario.html', {'form': form})

def adicionar_artigo(request):
    if request.method == 'POST':
        form = ArtigoForm(request.POST, request.FILES)
        if form.is_valid():
            artigo = form.save(commit=False)
            artigo.autor = request.user
            artigo.save()
            return redirect('artigos:artigos')
    else:
        form = ArtigoForm()
    return render(request, 'artigos/adicionar_artigo.html', {'form': form})



def custom_logout(request):
    logout(request)
    return redirect('artigos:registro')  # Redireciona para a página de registro após o logout

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

@login_required
def editar_artigo(request, artigo_id):
    artigo = get_object_or_404(Post, pk=artigo_id)
    if request.method == 'POST':
        form = ArtigoForm(request.POST, request.FILES, instance=artigo)
        if form.is_valid():
            form.save()
            return redirect('artigos:artigos')
    else:
        form = ArtigoForm(instance=artigo)
    return render(request, 'artigos/editar_artigo.html', {'form': form, 'artigo': artigo})


@login_required
def remover_artigo(request, artigo_id):
    artigo = get_object_or_404(Post, pk=artigo_id)

    if request.method == 'POST':
        artigo.delete()
        return redirect('artigos:artigos')

    return render(request, 'artigos/remover_artigo.html', {'artigo': artigo})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('artigos:artigos')  # Redireciona para a página principal após o login
    else:
        form = AuthenticationForm()
    return render(request, 'artigos/login.html', {'form': form})

def password_reset(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            return redirect('artigos:login')  # Redirecionar para a página de login após a redefinição de senha
        except User.DoesNotExist:
            # Tratar o caso em que o nome de usuário não existe
            return render(request, 'artigos/password_reset.html', {'error_message': 'Nome de usuário não encontrado. Por favor, tente novamente.'})
    else:
        return render(request, 'artigos/password_reset.html')

def artigos_view(request):
    artigos = Post.objects.annotate(avg_rating=Avg('rating__valor'))
    context = {'artigos': artigos}
    return render(request, 'artigos/artigos.html', context)
