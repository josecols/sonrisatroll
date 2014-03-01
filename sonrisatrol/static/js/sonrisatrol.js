/*  Sonrisatrol
    Aplicación: Sonrisatrol
    Aplicación URL: http://www.sonrisatrol.com
    Autor: José Cols - josecolsg@gmail.com
    Version: 1.0
    Requiere jQuery 1.9.1
*/
$(document).ready(function() {
	var menuActivo = false;
	$('#categorias').change(function() {
		if($(this).val() != "")
			window.location.href = $(this).val();
	});

	$('#cuenta').mouseenter(function() {
		abrirMenu();
	});

	$('#cuenta').mouseleave(function() {
		setTimeout(function() {
			cerrarMenu();
		}, 400);
	});

	$('#cuentaMenu').mouseenter(function() {
		menuActivo = true;
	});

	$('#cuentaMenu').mouseleave(function() {
		menuActivo = false;
		cerrarMenu();
	});

	function cerrarMenu() {
		if(menuActivo == false) {
			$('#cuentaMenu').css('display', 'none');
		}
	}

	function abrirMenu() {
		$('#cuentaMenu').css('display', 'block');
	}

	$('.compartir').click(function() {
		var id = $(this).attr('id').match(/[0-9]+/);
		if($('#sharebox' + id + '').is(':hidden')) {
			$(this).addClass('cseleccionado');
			$('#sharebox' + id + '').css('visibility', 'visible');
			$('#sharebox' + id + '').slideDown(200);
		} else {
			$('#sharebox' + id + '').slideUp(200);
			$(this).removeClass('cseleccionado');
		}
		return false;
	});
	$("[placeholder]").focus(function() {
		var e = $(this);
		if(e.val() == e.attr("placeholder")) {
			e.val("");
			e.removeClass("placeholder")
		}
	}).blur(function() {
		var e = $(this);
		if(e.val() == "" || e.val() == e.attr("placeholder")) {
			e.addClass("placeholder");
			e.val(e.attr("placeholder"))
		}
	}).blur().parents("form").submit(function() {
		$(this).find("[placeholder]").each(function() {
			var e = $(this);
			if(e.val() == e.attr("placeholder")) {
				e.val("")
			}
		})
	})
});

