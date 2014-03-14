#!/usr/bin/python
# -*- coding: utf-8 -*-

# Sonrisatrol - Django 1.4 - Python 2.7.3
# Desarrollado por José Cols - josecolsg@gmail.com - @josecols

from django import forms
from django.forms import widgets
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from models import Publicacion, PerfilUsuario, Seccion
from django.contrib.auth.forms import UserCreationForm


class RegistroUsuarioForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:

        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegistroUsuarioForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class PublicarImagenForm(forms.ModelForm):

    class Meta:

        model = Publicacion
        fields = ('titulo', 'imagen', 'etiquetas')

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
        fields = ('titulo', 'video', 'etiquetas')

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


class GhostWidget(widgets.Textarea):

    def render(
        self,
        name,
        value,
        attrs=None,
        ):

        return mark_safe(u'''
                <div class="editorwrap">
                    <section class="entry-markdown">
                        <header class="floatingheader">
                            &nbsp;&nbsp; Markdown
                        </header>
                        <section class="entry-markdown-content">
                            %s
                        </section>
                    </section>
                    <section class="entry-preview active">
                        <header class="floatingheader">
                            &nbsp;&nbsp; Resultado
                            <span class="entry-word-count">0 palabras</span>
                        </header>
                        <section class="entry-preview-content">
                            <div class="rendered-markdown"></div>
                        </section>
                    </section>
                </div>
                '''
                         % super(GhostWidget, self).render(name, value,
                         attrs={'id': 'entry-markdown'}))


class SeccionForm(forms.ModelForm):

    class Meta:

        model = Seccion
        widgets = {'contenido': GhostWidget}


