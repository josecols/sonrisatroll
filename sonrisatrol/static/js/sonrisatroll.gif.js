/*  Sonrisatroll
 	Aplicación: Sonrisatroll Reproductor GIF
	Aplicación URL: http://www.sonrisatroll.com
	Autor: José Cols - josecolsg@gmail.com - @josecols
	Version: 1.0
	Requiere jQuery 1.9.1
 */
var imagenes=[];function cache(src){var img=new Image();img.src=src;imagenes.push(img);}function control(img){if(img.attr('data-estado')=='estatico'){img.attr('src',img.attr('data-animado'));img.attr('data-estado','animado');img.css('visibility','hidden');img.siblings('.preloader').show();img.siblings('.reproducir').hide();}else{img.attr('src',img.attr('data-estatico'));img.attr('data-estado','estatico');img.siblings('.reproducir').show();}}function init(){$('.contenedor').each(function(){var ancho=$(this).width();var alto=$(this).height();$(this).children('.reproducir').css({top:(alto-65)/2+'px',left:(ancho-65)/2+'px'}).show();$(this).children('.preloader').css({top:(alto-64)/2+'px',left:(ancho-64)/2+'px'});$(this).children('.reproducir').click(function(){control($(this).siblings('.gif'));});});}$(window).load(function(){init();$(window).resize(function(){init();});$('.post .contenedor .gif').each(function(){$(this).click(function(){control($(this));});$(this).load(function(){if($(this).attr('data-estado')=='animado'){$(this).css('visibility','visible');$(this).siblings('.preloader').hide();cache($(this).attr('src'));}});});});