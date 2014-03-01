# encoding:utf-8
# Sonrisatrol - Django 1.4 - Python 2.7.3
# Desarrollado por José Cols - josecolsg@gmail.com - @josecols
from django import forms
from django.contrib.auth.models import User
from models import Publicacion, PerfilUsuario
from django.contrib.auth.forms import UserCreationForm
     
class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2") 
        
    def save(self, commit=True):
        user = super(RegistroUsuarioForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user   


class PublicarImagenForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = ("titulo", "imagen", "etiquetas") 
        
    def __init__(self, *args, **kwargs):
        self._autor = kwargs.pop('autor')
        
        super(PublicarImagenForm, self).__init__(*args, **kwargs)
    def save(self, commit=True):
        publicacion = super(PublicarImagenForm, self).save(commit=False)
        publicacion.autor = self._autor
        super_save_m2m = self.save_m2m
        def save_m2m():
            super_save_m2m()
            publicacion.etiquetas.clear()
            for etiqueta in self.cleaned_data['etiquetas']:
                publicacion.etiquetas.add(etiqueta)
        self.save_m2m = save_m2m
        if commit:
            publicacion.save()
            self.save_m2m()
        return publicacion   
        
        
class PublicarVideoForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = ("titulo", "video", "etiquetas")
        
    def __init__(self, *args, **kwargs):
        self._autor = kwargs.pop('autor')
        super(PublicarVideoForm, self).__init__(*args, **kwargs)
        
    def save(self, commit=True):
        publicacion = super(PublicarVideoForm, self).save(commit=False)
        publicacion.autor = self._autor
        super_save_m2m = self.save_m2m
        def save_m2m():
            super_save_m2m()
            publicacion.etiquetas.clear()
            for etiqueta in self.cleaned_data['etiquetas']:
                publicacion.etiquetas.add(etiqueta)
        self.save_m2m = save_m2m
        if commit:
            publicacion.save()
            self.save_m2m()
        return publicacion   


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')  
        
        
class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ('avatar', 'acerca', 'twitter', 'facebook')  
