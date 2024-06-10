from django.shortcuts import render
from .models import Praia, Regiao

def praias_view(request):
    regioes = Regiao.objects.all()
    context = {
        'regioes': regioes,
    }
    return render(request, 'praias/praias.html', context)

def praia_view(request, praia_nome):
    praia = Praia.objects.get(nome=praia_nome)
    context = {
        'praia': praia,
    }
    return render(request, 'praias/praia.html', context)
