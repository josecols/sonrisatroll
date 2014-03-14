/*  Sonrisatroll
    Aplicación: Sonrisatroll Navegación
    Aplicación URL: http://www.sonrisatroll.com
    Autor: José Cols - josecolsg@gmail.com - @josecols
    Version: 1.0
    Requiere jQuery 1.9.1
*/
$(document).ready(function(){$("#navegacion1").scroll();$(window).scroll(function(){lista=[];$(".post").each(function(index){if(index==longitud-1){var desplazamiento=$(this).offset().top-$(window).scrollTop()-350;}else{var desplazamiento=$(this).offset().top-$(window).scrollTop()-60;}lista.push(desplazamiento);});});$(document).keyup(function(event){if(String.fromCharCode(event.keyCode)=="j"||String.fromCharCode(event.keyCode)=="J"){var indice=publicacionActual()+1;$('html, body').animate({scrollTop:$("#navegacion"+indice+"").offset().top-56},100);}if(String.fromCharCode(event.keyCode)=="k"||String.fromCharCode(event.keyCode)=="K"){var indice=publicacionActual()-1;$('html, body').animate({scrollTop:$("#navegacion"+indice+"").offset().top-56},100);}});});var lista=[];var longitud=$(document).find('.post').length;function publicacionActual(){var indice=0;lista.sort();for(;indice<lista.length;++indice){if(lista[indice]>0){break;}}return indice;}