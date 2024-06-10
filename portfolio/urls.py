from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'portfolio'  # This defines the namespace

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.projects, name='projects'),
    path('technologies/', views.technologies, name='technologies'),
    path('logout/', auth_views.LogoutView.as_view(next_page='portfolio:registro'), name='logout'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro, name='registro'),
]
