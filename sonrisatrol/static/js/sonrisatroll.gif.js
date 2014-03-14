/*  Sonrisatroll
 	Aplicación: Sonrisatroll Reproductor GIF
	Aplicación URL: http://www.sonrisatroll.com
	Autor: José Cols - josecolsg@gmail.com - @josecols
	Version: 1.0
	Requiere jQuery 1.9.1
 */
$(window).load(function(){$(window).resize(function(){$('.contenedor').each(function(){var ancho=$(this).width();var alto=$(this).height();$(this).children('.reproducir').css({top:(alto-65)/2+'px',left:(ancho-65)/2+'px'}).show();});});$('.contenedor').each(function(){var ancho=$(this).width();var alto=$(this).height();$(this).children('.reproducir').css({top:(alto-65)/2+'px',left:(ancho-65)/2+'px'}).show();$(this).children('.reproducir').click(function(){control($(this).siblings('.gif'));});});$('.post .contenedor .gif').each(function(){$(this).click(function(){control(this);});});function control(img){if($(img).attr('data-estado')=='estatico'){$(img).attr('src',gifAnimado($(img).attr('src')));$(img).attr('data-estado','animado');$(img).siblings('.reproducir').hide();}else{$(img).attr('src',gifEstatico($(img).attr('src')));$(img).attr('data-estado','estatico');$(img).siblings('.reproducir').show();}}function gifEstatico(url){return url.split(".")[0]+"-static.png";}function gifAnimado(url){return url.split("-static")[0]+".gif";}});