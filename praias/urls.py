from django.urls import path
from . import views

app_name = 'praias'

urlpatterns = [
    path('', views.praias_view, name='praias'),  # Página inicial com lista de praias por região
    path('praia/<str:praia_nome>/', views.praia_view, name='praia'),  # Detalhes de uma praia específica
]
