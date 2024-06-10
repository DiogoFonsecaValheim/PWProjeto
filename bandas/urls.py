from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'bandas'

urlpatterns = [
    path('', views.bandas_view, name='bandas'),
    path('banda/<str:banda_nome>/', views.banda_view, name='banda'),
    path('banda/adicionar/', views.banda_adicionar, name='banda_adicionar'),
    path('banda/<int:pk>/editar/', views.banda_editar, name='banda_editar'),
    path('banda/<int:pk>/remover/', views.banda_remover, name='banda_remover'),
    path('album/adicionar/', views.album_adicionar, name='album_adicionar'),
    path('album/<int:pk>/editar/', views.album_editar, name='album_editar'),
    path('album/<int:pk>/remover/', views.album_remover, name='album_remover'),
    path('musica/<str:musica_titulo>/', views.musica_view, name='musica'),
    path('musica/adicionar/<str:banda_nome>/<str:album_titulo>/', views.musica_adicionar, name='musica_adicionar'),
    path('musica/<int:pk>/editar/', views.musica_editar, name='musica_editar'),
    path('musica/<int:pk>/remover/', views.musica_remover, name='musica_remover'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro, name='registro'),
    path('banda/<str:banda_nome>/album/<str:album_titulo>/', views.album_view, name='album'),
    path('logout/', auth_views.LogoutView.as_view(next_page='bandas:registro'), name='logout'),
]

