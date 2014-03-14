#!/usr/bin/python
# -*- coding: utf-8 -*-

# Sonrisatrol - Django 1.4 - Python 2.7.3
# Desarrollado por José Cols - josecolsg@gmail.com - @josecols

import re
import uuid
import os
from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save, pre_save, pre_delete, \
    m2m_changed


def directorio(instance, nombre):
    if isinstance(instance, PerfilUsuario):
        ruta = 'uploads/avatares'
    elif isinstance(instance, Publicacion):
        ruta = 'uploads/publicaciones'
    else:
        ruta = 'uploads/error'

    extension = nombre.split('.')[-1]
    nombre = '%s.%s' % (uuid.uuid4(), extension)
    return os.path.join(ruta, nombre)


def redimensionar(archivo, ancho_requerido):
    imagen = Image.open(archivo)
    (ancho, alto) = imagen.size
    if ancho > ancho_requerido:
        imagen.thumbnail((ancho_requerido, alto), Image.ANTIALIAS)
        imagen.save(archivo)


def gif_animado(archivo):
    extension = archivo.split('.')[-1]
    if extension.upper() == 'GIF':
        gif = Image.open(archivo)
        try:
            gif.seek(1)
        except EOFError:
            gif.close()
            return False
        else:
            return True
    return False


class Seccion(models.Model):

    titulo = models.CharField(max_length=100, unique=True,
                              verbose_name="título")
    contenido = \
        models.TextField(help_text='Ingrese información relacionada a la sección'
                         )
    slug = models.SlugField(max_length=100, editable=False)

    class Meta:

        verbose_name = "sección"
        verbose_name_plural = 'secciones'

    def __unicode__(self):
        return self.titulo

    def save(self):
        if not self.id:
            self.slug = slugify(self.titulo)
        super(Seccion, self).save()


class Etiqueta(models.Model):

    titulo = models.CharField(max_length=50, unique=True,
                              verbose_name="título")

    def __unicode__(self):
        return self.titulo


class Medalla(models.Model):

    titulo = models.CharField(max_length=100, unique=True,
                              verbose_name="título")
    descripcion = models.TextField(verbose_name="descripción")
    icono = models.ImageField(upload_to='uploads/medallas')

    def __unicode__(self):
        return self.titulo


class Rango(models.Model):

    titulo = models.CharField(max_length=100, unique=True,
                              verbose_name="título")
    descripcion = models.TextField(verbose_name="descripción")
    icono = models.ImageField(upload_to='uploads/rangos')
    valor = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.titulo


class Publicacion(models.Model):

    autor = models.ForeignKey(User)
    titulo = models.CharField(max_length=100, verbose_name="título")
    slug = models.SlugField(max_length=100, editable=False)
    imagen = models.ImageField(upload_to=directorio, blank=True)
    video = models.URLField(help_text='URL del vídeo en YouTube',
                            blank=True, verbose_name="vídeo")
    favoritos = models.PositiveIntegerField(default=0, editable=False)
    etiquetas = models.ManyToManyField(Etiqueta)
    aprobado = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:

        verbose_name = "publicación"
        verbose_name_plural = 'publicaciones'

    def __unicode__(self):
        return self.titulo

    def is_youtube_url(self):
        return re.search(r'^(http|https)\:\/\/www\.youtube\.com\/watch\?v\=(\w*)(\&(.*))?$'
                         , self.video)

    def save(self):
        if not self.id:
            self.slug = slugify(self.titulo)
        super(Publicacion, self).save()
        if self.imagen:
            archivo = self.imagen.path
            if gif_animado(archivo):
                gif = Image.open(archivo)
                png = Image.new('RGBA', gif.size)
                png.paste(gif)
                png.save(archivo.split('.')[0] + '-static.png')
                archivo = archivo.split('.')[0] + '-static.png'
            redimensionar(archivo, 760)

    def clean(self):
        if not self.imagen and not self.video:
            raise ValidationError("Debe registrar una imagen o un vídeo."
                                  )
        elif self.imagen and self.video:
            raise ValidationError("Sólo puede registrar un elemento, imagen o vídeo."
                                  )
        if not self.imagen and not self.is_youtube_url():
            raise ValidationError("La URL del vídeo no es válida.")


class PerfilUsuario(models.Model):

    user = models.OneToOneField(User, unique=True, related_name='perfil'
                                )
    avatar = models.ImageField(upload_to=directorio, blank=True)
    acerca = models.TextField(verbose_name="acerca de mí", blank=True)
    twitter = models.CharField(max_length=15,
                               help_text='Ingresa tu usuario en Twitter sin el @'
                               , blank=True)
    facebook = \
        models.URLField(help_text='Ingresa la URL completa de tu perfil en Facebook'
                        , blank=True)
    puntos = models.PositiveIntegerField(default=0)
    rango = models.ForeignKey(Rango, null=True, blank=True)
    medallas = models.ManyToManyField(Medalla, blank=True)
    publicaciones = models.ManyToManyField(Publicacion, blank=True)
    favoritos = models.ManyToManyField(Publicacion, blank=True,
            related_name='usuario_favoritos')

    class Meta:

        verbose_name = 'perfil de usuario'
        verbose_name_plural = 'perfiles de usuario'

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super(PerfilUsuario, self).save(*args, **kwargs)
        if self.avatar:
            redimensionar(self.avatar.path, 150)
        else:
            self.avatar = 'uploads/avatares/avatar.png'
            super(PerfilUsuario, self).save(*args, **kwargs)


def crear_perfil(
    sender,
    instance,
    created,
    **kwargs
    ):
    if created:
        created = PerfilUsuario.objects.get_or_create(user=instance)


def asignar_rango(sender, instance, **kwargs):
    try:
        rango = Rango.objects.get(valor=instance.puntos)
    except Rango.DoesNotExist:
        rango = None
    if rango:
        instance.rango = rango


def asignar_medallas(sender, instance, **kwargs):
    medalla = None
    try:
        if Publicacion.objects.filter(autor=instance.autor,
                aprobado=True).count() == 100:
            medalla = Medalla.objects.get(titulo="Sangre de bufón")
        elif Publicacion.objects.filter(autor=instance.autor,
                aprobado=True).count() == 1:
            medalla = Medalla.objects.get(titulo='Un trol ha nacido')
    except Medalla.DoesNotExist:
        medalla = None
    if medalla:
        PerfilUsuario.objects.get(user=instance.autor).medallas.add(medalla)


def usuario_autenticado(
    sender,
    user,
    request,
    **kwargs
    ):
    dias = (user.last_login - user.date_joined).days
    if dias >= 365:
        try:
            medalla = \
                Medalla.objects.get(titulo='El tiempo vuela cuando te diviertes'
                                    )
        except Medalla.DoesNotExist:
            medalla = None
        if medalla:
            PerfilUsuario.objects.get(user=user).medallas.add(medalla)


def borrar_publicacion(sender, instance, **kwargs):
    os.remove(instance.imagen.path)
    try:
        os.remove(instance.imagen.path.split('.')[0] + '-static.png')
    except OSError:
        pass


def agregar_etiqueta(
    sender,
    instance,
    action,
    **kwargs
    ):
    if action == 'post_clear' and instance.imagen \
        and gif_animado(instance.imagen.path):
        instance.etiquetas.add(Etiqueta.objects.get(titulo='GIF'))


# Señales

post_save.connect(crear_perfil, sender=User)
pre_save.connect(asignar_rango, sender=PerfilUsuario)
post_save.connect(asignar_medallas, sender=Publicacion)
pre_delete.connect(borrar_publicacion, sender=Publicacion)
m2m_changed.connect(agregar_etiqueta,
                    sender=Publicacion.etiquetas.through)
user_logged_in.connect(usuario_autenticado)
