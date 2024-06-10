from django.db import models

class Autor(models.Model):
    nome = models.CharField(max_length=50)
    ano_nascimento = models.IntegerField()
    nacionalidade = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class Livro(models.Model):
    titulo = models.CharField(max_length=50)
    autor = models.ForeignKey(Autor,on_delete=models.CASCADE)
    genero = models.CharField(max_length=50)
    ano_publicacao = models.IntegerField()


    def __str__(self):
        return f"{self.titulo} ({self.autor})"