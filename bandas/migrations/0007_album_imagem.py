# Generated by Django 4.0.6 on 2024-04-18 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bandas', '0006_alter_musicas_ano'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='imagem',
            field=models.ImageField(default='home/a22204579/project/artigos/receba.jpg', upload_to=''),
        ),
    ]
