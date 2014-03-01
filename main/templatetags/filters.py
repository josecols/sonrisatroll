#encoding:utf-8
import re
from django import template
register = template.Library()

# Convierte una URL de youtube a HTML embebido.
@register.filter(name='youtube_embed_url')
def youtube_embed_url(url):
    match = re.search(r'^(http|https)\:\/\/www\.youtube\.com\/watch\?v\=(\w*)(\&(.*))?$', url)
    if match:
        embed_url = 'http://www.youtube.com/embed/%s' % (match.group(2))
        result = "<div class=\"video-container\"><iframe width=\"470\" height=\"315\" src=\"%s\" frameborder=\"0\" allowfullscreen></iframe></div>" % (embed_url)
        return result
    return ''
youtube_embed_url.is_safe = True

# Toma la URL de un vídeo en youtube y regresa el thumbnail correspondiente a ese vídeo
@register.filter(name='youtube_thumbnail')
def youtube_thumbnail(url):
    match = re.search(r'^(http|https)\:\/\/www\.youtube\.com\/watch\?v\=(\w*)(\&(.*))?$', url)
    if match:        
        result = "http://img.youtube.com/vi/%s/2.jpg" % (match.group(2))
        return result
    return ''

# Abrevia un valor numérico de forma amigable
@register.filter(name='cuenta')
def cuenta(n):
    resultado = str(n)
    if n > 999:
        resultado = "1K"
    elif n > 9999:
        resultado = "10K"
    elif n > 99999:
        resultado = "100K"
    return resultado

# Determina una medalla para el contador según el valor de la cuenta
@register.filter(name='contador')
def contador(cuenta):
    resultado = "bronce"
    if cuenta > 999:
        resultado = "plata"
    elif cuenta > 9999:
        resultado = "oro"
    return resultado

# Convierte el dominio de la página en una URL con HTTP
@register.filter(name='weburl')
def weburl(dominio):
    return "http://{}/".format(dominio)

# Retorna la imagen estática asociada a un GIF
@register.filter(name='gif_estatico')
def gif_estatico(url):
    return url.split('.')[0] + "-static.png"