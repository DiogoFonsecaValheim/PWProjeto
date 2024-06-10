from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    titulo = models.CharField(max_length=1000)
    data = models.DateTimeField(verbose_name="Data de Publicação")
    foto = models.ImageField()
    texto = models.TextField()  # Adicione este campo

    def __str__(self):
        return f'Titulo: {self.titulo}'

    def comentarios(self):
        return Comen.objects.filter(post=self)

class Comen(models.Model):
    nome = models.CharField(max_length=300)
    titulo = models.CharField(max_length=30000)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'Nome: {self.nome}, Artigo: {self.post.titulo}'

class Rating(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    valor = models.IntegerField()

    def __str__(self):
        return f'Rating: {self.valor}, Artigo: {self.post.titulo}'