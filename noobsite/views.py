from django.shortcuts import render

from django.http import HttpResponse

def index_view(request):
    return HttpResponse("Olá n00b, esta é a página web mais básica do mundo!")

def nome_view(request):
    return HttpResponse("receba")

def telmo_view(request):
    return HttpResponse("Odeio o Telmo")

def jeff_view(request):
    return HttpResponse("Jeffrey Epstein")
