from bandas.models import *
import json

Banda.objects.all().delete()

Musicas.objects.all().delete()

Album.objects.all().delete()

with open('bandas/json/bandas.json') as f:
    bandas = json.load(f)

    for banda_info in bandas:
        print(banda_info)  # teste
        Banda.objects.create(
            nome=banda_info.get('nome', 'Nome desconhecido'),
            ano_criacao=banda_info.get('ano_lancamento', '0000'),
            nacionalidade=banda_info.get('nacionalidade', 'Desconhecido')
        )

with open('bandas/json/musicas.json') as f:
    albuns = json.load(f)

    for album_info in albuns:
        # Primeiro, criamos o álbum
        album = Album.objects.create(
            titulo=album_info['titulo'],
            ano_lancamento=album_info['ano_lancamento'],
            banda=Banda.objects.get(nome=album_info['banda'])
        )
        print(album_info)
        # Em seguida, percorremos as músicas dentro do álbum
        for musica_info in album_info['musicas']:
            Musicas.objects.create(
                titulo=musica_info['titulo'],
                duracao=musica_info['duracao'],
                album=album
            )