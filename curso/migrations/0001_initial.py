# Generated by Django 4.0.6 on 2024-04-21 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area_Cientifica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome')),
            ],
        ),
        migrations.CreateModel(
            name='Disciplina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome')),
                ('ano', models.IntegerField(verbose_name='Ano')),
                ('semestre', models.IntegerField(verbose_name='Semestre')),
                ('ects', models.IntegerField(verbose_name='Ects')),
                ('code', models.IntegerField(verbose_name='curricularIUnitReadableCode')),
                ('conteudos', models.CharField(default='Conteúdos Programáticos Padrão', max_length=500, verbose_name='Conteúdos Programáticos')),
                ('area_cientifica', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='curso.area_cientifica')),
            ],
        ),
        migrations.CreateModel(
            name='Linguagem_Programacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome')),
            ],
        ),
        migrations.CreateModel(
            name='Projeto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome')),
                ('descricao', models.TextField(verbose_name='Descrição')),
                ('conceitos', models.TextField(verbose_name='Conceitos Aplicados')),
                ('tecnologias', models.TextField(verbose_name='Tecnologias Usadas')),
                ('foto', models.ImageField(upload_to='', verbose_name='Imagem do Projeto')),
                ('video', models.URLField(null=True, verbose_name='Link Video do Youtube')),
                ('gitLink', models.URLField(null=True, verbose_name='Link Repositório GitHub')),
                ('disciplina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='curso.disciplina')),
                ('linguagens', models.ManyToManyField(to='curso.linguagem_programacao', verbose_name='Linguagens de Programação')),
            ],
        ),
        migrations.CreateModel(
            name='Docente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome')),
                ('disciplina', models.ManyToManyField(to='curso.disciplina', verbose_name='Disciplina/s')),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome')),
                ('apresentacao', models.TextField(verbose_name='Apresentação')),
                ('objetivos', models.TextField(verbose_name='Objetivos')),
                ('competencias', models.TextField(verbose_name='Competências')),
                ('disciplinas', models.ManyToManyField(related_name='cursos', to='curso.disciplina', verbose_name='Disciplinas')),
            ],
        ),
    ]
