from django import forms
from .models import Post, Comen, Rating  # Importe os modelos do seu aplicativo 'artigos'
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import TextInput
from django.contrib.auth.models import User

class ComenForm(forms.ModelForm):
    class Meta:
        model = Comen
        fields = ['nome', 'titulo']

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['valor']

class CustomDateTimeInput(TextInput):
    input_type = 'datetime-local'

class ArtigoForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'data', 'foto', 'texto']  # Adicione o campo 'texto'
        widgets = {
            'data': CustomDateTimeInput(),
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')
