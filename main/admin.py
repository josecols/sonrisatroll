#!/usr/bin/python
# -*- coding: utf-8 -*-

# Sonrisatrol - Django 1.4 - Python 2.7.3
# Desarrollado por José Cols - josecolsg@gmail.com - @josecols

from django.contrib import admin
from models import Seccion, Etiqueta, Medalla, Rango, Publicacion, \
    PerfilUsuario
from forms import SeccionForm


class PublicacionAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(
        self,
        db_field,
        request,
        **kwargs
        ):

        if db_field.name == 'autor':
            kwargs['initial'] = request.user.id
            return db_field.formfield(**kwargs)
        return super(PublicacionAdmin,
                     self).formfield_for_foreignkey(db_field, request,
                **kwargs)

    list_display = ('titulo', 'favoritos', 'aprobado')
    search_fields = ('titulo', 'etiquetas')
    list_filter = ('aprobado', )


class SeccionAdmin(admin.ModelAdmin):

    form = SeccionForm

    class Media:

        css = {'all': ('/static/js/ghost/ghostdown.css', )}
        js = ('/static/js/jquery-1.10.2.min.js',
              '/static/js/ghost/ghostdown.js')


admin.site.register(Seccion, SeccionAdmin)
admin.site.register(Etiqueta)
admin.site.register(Medalla)
admin.site.register(Rango)
admin.site.register(Publicacion, PublicacionAdmin)
admin.site.register(PerfilUsuario)

