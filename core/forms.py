from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Libro


class RegistroUsuarioForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',)


class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ('titulo', 'autor', 'portada')
        labels = {
            'titulo': 'Título del libro',
            'autor': 'Autor o autora',
            'portada': 'Imagen de portada (opcional)',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={
                'placeholder': 'Ej. Cien años de soledad',
                'autocomplete': 'off',
                'autofocus': True,
            }),
            'autor': forms.TextInput(attrs={
                'placeholder': 'Ej. Gabriel García Márquez',
                'autocomplete': 'off',
            }),
            'portada': forms.ClearableFileInput(attrs={
                'accept': 'image/*',
            }),
        }
