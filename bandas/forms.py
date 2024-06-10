from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Banda, Album, Musicas

class BandaForm(forms.ModelForm):
    class Meta:
        model = Banda
        fields = '__all__'

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['titulo', 'ano_lancamento', 'banda', 'imagem']

class MusicaForm(forms.ModelForm):
    class Meta:
        model = Musicas
        fields = ['titulo', 'duracao', 'letra']  # Inclua o campo letra
        widgets = {
            'album': forms.HiddenInput(),  # Campo oculto para o ID do álbum
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')
