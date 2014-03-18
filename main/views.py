# encoding:utf-8
# Sonrisatrol - Django 1.4 - Python 2.7.3
# Desarrollado por José Cols - josecolsg@gmail.com - @josecols
from django.db.models import Q
from django.http import Http404
from django.utils import simplejson
from django.http import HttpResponse
from templatetags import filters
from django.shortcuts import redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render_to_response, get_object_or_404
from models import Publicacion, PerfilUsuario, Seccion, Rango, Medalla
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from forms import RegistroUsuarioForm, PublicarImagenForm, PublicarVideoForm, UsuarioForm, PerfilUsuarioForm

# Publicaciones por página
PUBLICACIONES = 10

def paginar(lista, pagina, items):
    paginator = Paginator(lista, items)
    try:
        publicaciones = paginator.page(pagina)
    except PageNotAnInteger:
        publicaciones = paginator.page(1)
    except EmptyPage:
        publicaciones = paginator.page(paginator.num_pages)
    return publicaciones

def asignar_medalla(usuario, titulo):
    medalla = Medalla.objects.get(titulo=titulo)
    if medalla:
        usuario.medallas.add(medalla)

def aviso(request, mensaje, exito):
    request.session['mensaje'] = mensaje
    request.session['exito_mensaje'] = exito
    return request

@csrf_protect
def favorito(request):
    if request.method == 'POST':
        publicacion = get_object_or_404(Publicacion, pk=request.POST.get('publicacion_id', None))
        usuario = PerfilUsuario.objects.get(user=request.user)
        autor = PerfilUsuario.objects.get(user=publicacion.autor)

        if publicacion in usuario.favoritos.all():
            autor.puntos -= 1
            publicacion.favoritos -= 1
            usuario.favoritos.remove(publicacion)
        else:
            autor.puntos += 1
            publicacion.favoritos += 1
            usuario.favoritos.add(publicacion)

        publicacion.save()
        usuario.save()
        autor.save()

        # Medalla
        if usuario.favoritos.all().count() == 1000:
            try:
                medalla = Medalla.objects.get(titulo="Sonrisa de guasón")
            except Rango.DoesNotExist:
                medalla = None
            if medalla:
                usuario.medallas.add(medalla)

        return HttpResponse(simplejson.dumps(filters.cuenta(publicacion.favoritos)), mimetype='application/javascript')
    raise Http404

def index(request, categoria="nuevo", pagina="1", mensaje=None):
    if categoria == "popular":
        lista = Publicacion.objects.filter(aprobado=True).order_by('favoritos').reverse()
    elif categoria == 'nuevo':
        lista = Publicacion.objects.filter(aprobado=True).order_by('fecha').reverse()
    else:
        raise Http404

    publicaciones = paginar(lista, pagina, PUBLICACIONES)
    return render_to_response('index.html',
                              {'publicaciones':publicaciones, 'categoria':categoria, 'request':request},
                              context_instance=RequestContext(request))

def usuario(request, username, categoria="aportes", pagina="1"):
    user = get_object_or_404(User, username=username)
    perfil = PerfilUsuario.objects.get(user=user)
    if categoria == "aportes":
        lista = Publicacion.objects.filter(autor=user, aprobado=True).order_by('fecha').reverse()
        favoritos = None
    elif categoria == "favoritos":
        lista = perfil.favoritos.all()
        favoritos = not None
    else:
        raise Http404

    publicaciones = paginar(lista, pagina, PUBLICACIONES)
    return render_to_response('usuario.html',
                              {'perfil':perfil, 'publicaciones':publicaciones, 'favoritos':favoritos, 'request':request},
                              context_instance=RequestContext(request))

def seccion(request, slug):
    seccion = get_object_or_404(Seccion, slug=slug)
    return render_to_response('seccion.html',
                              {'seccion':seccion, 'request':request},
                              context_instance=RequestContext(request))

def publicacion(request, slug, post_id):
    publicacion = get_object_or_404(Publicacion, pk=post_id)
    return render_to_response('publicacion.html',
                              {'publicacion':publicacion, 'request':request},
                              context_instance=RequestContext(request))

def busqueda(request, pagina="1", query=None):
    if not query:
        query = request.GET.get('q', '')
        if query:
            qset = (Q(titulo__icontains=query) | Q(etiquetas__titulo__icontains=query))
            lista = Publicacion.objects.filter(qset).distinct()
            resultados = paginar(lista, pagina, PUBLICACIONES * 2)
        else:
            resultados = None

    return render_to_response('busqueda.html',
                              {'resultados': resultados, 'query': query, 'request':request},
                              context_instance=RequestContext(request))

# Vistas dinámicas de usuario
@login_required(login_url='/autenticacion')
def publicar(request, tipo_publicacion="imagen"):
    if tipo_publicacion == "imagen":
        if request.method == 'POST':
                formulario = PublicarImagenForm(request.POST, request.FILES, autor=request.user)
                if formulario.is_valid():
                    formulario.save()
                    return redirect('index')
        else:
            formulario = PublicarImagenForm(autor=request.user)

    else:
        if request.method == 'POST':
            formulario = PublicarVideoForm(request.POST, autor=request.user)
            if formulario.is_valid():
                formulario.save()
                return redirect('index')
        else:
            formulario = PublicarVideoForm(autor=request.user)

    return render_to_response('publicar.html',
                              {'formulario':formulario, 'request':request},
                              context_instance=RequestContext(request))

@login_required(login_url='/autenticacion')
def editar_perfil(request):
    usuario = PerfilUsuario.objects.get(user=request.user)

    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST, instance=request.user)
        perfil_form = PerfilUsuarioForm(request.POST, request.FILES, instance=request.user.perfil)
        if usuario_form.is_valid() and perfil_form.is_valid():
            usuario_form.save()
            perfil_form.save()
            aviso(request, '¡Éxito! El usuario se ha modificado correctamente', True)
            return redirect('index')
    else:
        usuario_form = UsuarioForm(instance=request.user)
        perfil_form = PerfilUsuarioForm(instance=request.user.perfil)

    return render_to_response('editar-perfil.html',
                              { 'usuario_form': usuario_form, 'perfil_form': perfil_form, 'request':request },
                              context_instance=RequestContext(request))

def registro(request):
    if request.user.is_authenticated():
        return redirect('index')

    if request.method == 'POST':
        formulario = RegistroUsuarioForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            aviso(request, '¡Éxito! El usuario se ha creado, ya puedes iniciar sesión', True)
            return redirect('index')
    else:
        formulario = RegistroUsuarioForm()

    return render_to_response('registro.html',
                              {'formulario':formulario},
                              context_instance=RequestContext(request))

def autenticacion(request, error=None):
    if request.user.is_authenticated():
        return redirect('index')

    if request.method == 'POST':
        formulario = AuthenticationForm()
        usuario = authenticate(username=request.POST['username'], password=request.POST['password'])
        if usuario is not None:
            if usuario.is_active:
                login(request, usuario)
            else:
                aviso(request, '¡Error! El usuario se encuentra desactivado', False)
            return redirect('index')
        else:
            return render_to_response('autenticacion.html',
                                      {'formulario':formulario, 'error':'¡Error! El usuario y la contraseña no coinciden'},
                                      context_instance=RequestContext(request))

    formulario = AuthenticationForm()
    return render_to_response('autenticacion.html',
                              {'formulario':formulario},
                              context_instance=RequestContext(request))

@csrf_protect
def borrar_mensaje(request):
    if request.method == 'POST':
        request.session['mensaje'] = request.session['exito_mensaje'] = None

def salir(request):
    logout(request)
    return redirect('index')

# Google webmaster tools
def google(request):
    return render_to_response('google7076d88b2720fcc5.html',
                              {'request':request},
                              context_instance=RequestContext(request))
