# Generated by Django 4.0.6 on 2024-04-06 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bandas', '0005_alter_musicas_duracao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='musicas',
            name='ano',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
