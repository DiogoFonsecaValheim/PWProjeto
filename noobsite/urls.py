# noobsite/urls.py

from django.urls import path
from . import views  # importamos views para poder usar as suas funções

urlpatterns = [
    path('index/', views.index_view),
    path('Receba/', views.nome_view),
    path('Telmo/', views.telmo_view),
    path('Jeff/', views.jeff_view),
]