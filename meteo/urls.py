from django.urls import path
from . import views

urlpatterns = [
    path('', views.today_weather, name='today_weather'),
    path('5days/', views.five_days_weather, name='five_days_weather'),
    path('five-days/', views.five_days_weather, name='five_days_weather'),
    path('previsao-hoje/', views.previsao_hoje, name='previsao_hoje'),
    path('previsao-5-dias/', views.previsao_5_dias, name='previsao_5_dias'),
    path('lista_cidades/', views.lista_cidades, name='lista_cidades'),
]