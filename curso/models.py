from django.db import models

class Curso(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome')
    apresentacao = models.TextField(verbose_name='Apresentação')
    objetivos = models.TextField(verbose_name='Objetivos')
    competencias = models.TextField(verbose_name='Competências')
    disciplinas = models.ManyToManyField('Disciplina', related_name='cursos', verbose_name='Disciplinas')

    def __str__(self):
        return f'Nome: {self.nome}'

class Area_Cientifica(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome')

    def __str__(self):
        return f'Área Ciêntifica: {self.nome}'

class Linguagem_Programacao(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome')

    def __str__(self):
        return f'Nome: {self.nome}'

class Disciplina(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome')
    ano = models.IntegerField(verbose_name='Ano')
    semestre = models.IntegerField(verbose_name='Semestre')
    ects = models.IntegerField(verbose_name='Ects')
    code = models.IntegerField(verbose_name='curricularIUnitReadableCode')
    conteudos = models.CharField(max_length=500, verbose_name='Conteúdos Programáticos', default='Conteúdos Programáticos Padrão')
    area_cientifica = models.ForeignKey('Area_Cientifica', on_delete=models.CASCADE)

    def __str__(self):
        return f'Nome: {self.nome}'

class Projeto(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome')
    descricao = models.TextField(verbose_name='Descrição')
    conceitos = models.TextField(verbose_name='Conceitos Aplicados')
    tecnologias = models.TextField(verbose_name='Tecnologias Usadas')
    foto = models.ImageField(verbose_name='Imagem do Projeto')
    video = models.URLField(null=True, verbose_name='Link Video do Youtube')
    gitLink = models.URLField(null=True, verbose_name='Link Repositório GitHub')
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    linguagens = models.ManyToManyField(Linguagem_Programacao, verbose_name='Linguagens de Programação')

    def __str__(self):
        return f'Nome: {self.nome}'

class Docente(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome')
    disciplina = models.ManyToManyField(Disciplina, verbose_name='Disciplina/s')

    def __str__(self):
        return f'Nome: {self.nome}'
