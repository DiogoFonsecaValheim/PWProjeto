from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'curso'

urlpatterns = [
    path('', views.lista_cursos, name='lista_cursos'),
    path('curso/<str:curso_nome>/', views.detalhes_curso, name='detalhes_curso'),
    path('disciplina/<str:disciplina_nome>/', views.detalhes_disciplina, name='detalhes_disciplina'),
    path('projeto/<str:projeto_nome>/', views.detalhes_projeto, name='detalhes_projeto'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro, name='registro'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('logout/', auth_views.LogoutView.as_view(next_page='cursos:registro'), name='logout'),
]