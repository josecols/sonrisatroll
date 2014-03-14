/*  Sonrisatroll
    Aplicación: Sonrisatroll Placeholder
    Aplicación URL: http://www.sonrisatroll.com
    Autor: José Cols - josecolsg@gmail.com - @josecols
    Version: 1.0
    Requiere jQuery 1.9.1
*/
$(document).ready(function(){$("[placeholder]").focus(function(){var e=$(this);if(e.val()==e.attr("placeholder")){e.val("");e.removeClass("placeholder");}}).blur(function(){var e=$(this);if(e.val()==""||e.val()==e.attr("placeholder")){e.addClass("placeholder");e.val(e.attr("placeholder"));}}).blur().parents("form").submit(function(){$(this).find("[placeholder]").each(function(){var e=$(this);if(e.val()==e.attr("placeholder")){e.val("")}});});});