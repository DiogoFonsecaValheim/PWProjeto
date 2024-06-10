from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'artigos'

urlpatterns = [
    path('', views.artigos_view, name='artigos'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro, name='registro'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('logout/', auth_views.LogoutView.as_view(next_page='artigos:registro'), name='logout'),
    path('adicionar_comentario/<int:post_id>/', views.adicionar_comentario, name='adicionar_comentario'),
    path('editar_comentario/<str:comentario_texto>/', views.editar_comentario, name='editar_comentario'),
    path('visualizar_comentarios/<int:post_id>/', views.visualizar_comentarios, name='visualizar_comentarios'),
    path('remover_comentario/<str:comentario_texto>/', views.remover_comentario, name='remover_comentario'),
     path('remover_rating/<int:rating_id>/', views.remover_rating, name='remover_rating'),
    path('editar_rating/<int:rating_id>/', views.editar_rating, name='editar_rating'),
    path('adicionar_rating/<int:post_id>/', views.adicionar_rating, name='adicionar_rating'),
    path('gerir_ratings/<int:artigo_id>/', views.gerir_ratings, name='gerir_ratings'),
    path('adicionar/', views.adicionar_artigo, name='adicionar_artigo'),
     path('editar_artigo/<int:artigo_id>/', views.editar_artigo, name='editar_artigo'),
    path('remover_artigo/<int:artigo_id>/', views.remover_artigo, name='remover_artigo'),
]
