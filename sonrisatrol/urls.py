#encoding:utf-8
from django.contrib import admin
from django.conf import settings
from django.conf.urls import patterns, include, url
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'main.views.index', name='index'),
    url(r'^categoria/(?P<categoria>[-\w]+)/$', 'main.views.index', name='index_categoria'),
    url(r'^categoria/(?P<categoria>[-\w]+)/pagina-(?P<pagina>\d+)/$', 'main.views.index', name='index_pagina'),
    url(r'^favorito/$', 'main.views.favorito', name='favorito'),
    url(r'^usuario/(?P<username>[-\w]+)/(?P<categoria>[-\w\d]+)-(?P<pagina>\d+)/$', 'main.views.usuario', name='usuario'),
    url(r'^usuario/(?P<username>[-\w]+)/$', 'main.views.usuario'),
    url(r'^seccion/(?P<slug>[-\w]+)/$', 'main.views.seccion', name='seccion'),
    url(r'^publicacion/(?P<slug>[-\w\d]+)-(?P<post_id>\d+)/$', 'main.views.publicacion' , name='publicacion'),
    url(r'^busqueda-(?P<pagina>\d+)/$', 'main.views.busqueda', name='busqueda'),
    url(r'^busqueda-(?P<pagina>\d+)/(?P<query>[-\w]+)/$', 'main.views.busqueda', name='busqueda_query'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT, }),
    # URL para vistas dinámicas de usuarios
    url(r'^publicar/$', 'main.views.publicar'),
    url(r'^publicar/(?P<tipo_publicacion>[-\w]+)$', 'main.views.publicar', name='publicar'),
    url(r'^borrar-mensaje/$', 'main.views.borrar_mensaje', name='borrar_mensaje'),
    url(r'^registro/$', 'main.views.registro', name='registro'),
    url(r'^autenticacion/$', 'main.views.autenticacion', name='autenticacion'),
    url(r'^salir/$', 'main.views.salir', name='salir'),
    url(r'^cuenta/editar-perfil/$', 'main.views.editar_perfil', name='editar-perfil'),
    url(r'^cuenta/restablecer-clave/$', 'django.contrib.auth.views.password_reset',
        {'post_reset_redirect' : '/cuenta/restablecer-clave/exito/'}, name='restablecer-clave'),
    url(r'^cuenta/restablecer-clave/exito/$', 'django.contrib.auth.views.password_reset_done'),
    url(r'^cuenta/restablecer-clave/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)/$', 'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect' : '/cuenta/restablecer-clave/completado/'}),
    url(r'^cuenta/restablecer-clave/completado/$', 'django.contrib.auth.views.password_reset_complete'),
    # Administración
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Google webmaster tools
    url(r'^google7076d88b2720fcc5.html$', 'main.views.google', name='google'),
    # Google Auth
    url(r'^google/autenticacion/$', 'main.views.google_autenticacion', name='google_autenticacion'),
)
