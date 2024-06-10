# urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'cursos'

urlpatterns = [
    path('', views.lista_cursos, name='lista_cursos'),
    path('adicionar_curso/', views.adicionar_curso, name='adicionar_curso'),
    path('curso/<str:curso_nome>/adicionar_disciplina/', views.adicionar_disciplina, name='adicionar_disciplina'),
    path('curso/<str:curso_nome>/', views.detalhes_curso, name='detalhes_curso'),
    path('curso/<str:curso_nome>/editar/', views.editar_curso, name='editar_curso'),
    path('curso/<str:curso_nome>/remover/', views.remover_curso, name='remover_curso'),
    path('disciplina/<str:disciplina_nome>/', views.detalhes_disciplina, name='detalhes_disciplina'),
    path('disciplina/<str:disciplina_nome>/editar/', views.editar_disciplina, name='editar_disciplina'),
    path('disciplina/<str:disciplina_nome>/remover/', views.remover_disciplina, name='remover_disciplina'),
    path('disciplina/<str:disciplina_nome>/adicionar_projeto/', views.adicionar_projeto, name='adicionar_projeto'),
    path('projeto/<str:projeto_nome>/', views.detalhes_projeto, name='detalhes_projeto'),
    path('projeto/<str:projeto_nome>/editar/', views.editar_projeto, name='editar_projeto'),
    path('projeto/<str:projeto_nome>/remover/', views.remover_projeto, name='remover_projeto'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro, name='registro'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('logout/', auth_views.LogoutView.as_view(next_page='cursos:registro'), name='logout'),
]
