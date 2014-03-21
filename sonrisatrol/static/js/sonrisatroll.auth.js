/*  Sonrisatroll
    Aplicación: Sonrisatroll Auth
    Aplicación URL: http://www.sonrisatroll.com
    Autor: José Cols - josecolsg@gmail.com
    Version: 1.0
    Requiere jQuery 1.9.1
*/
function signinCallback(authResult) {
    if (authResult) {
        if (authResult['error'] == undefined) {
            gapi.auth.setToken(authResult);
            consultarInfo();
        } else {
            console.log('Error');
        }
    } else {
        console.log('authResult vacío');
    }
}

function consultarInfo() {
    gapi.client.load('oauth2', 'v2', function () {
        var request = gapi.client.oauth2.userinfo.get();
        request.execute(construirData);
    });
}

function generarUsuario(nombre) {
    usuario = nombre.split(' ');
    if (usuario.length > 2)
        usuario = usuario[0] + usuario[2];
    else
        usuario = usuario[0] + usuario[1];
    return usuario;
}

function construirData(obj) {
    var data = {
        'usuario': generarUsuario(obj['name']),
        'email': obj['email'] == undefined ? 'None' : obj['email'],
        'nombre': obj['given_name'],
        'apellido': obj['family_name'],
        'id': obj['id'],
        'avatar': obj['picture'],
        'csrfmiddlewaretoken': csrfToken,
    }
    autenticar(data);
}

function autenticar(usuario) {
    var request = $.ajax({
        async: true,
        type: 'POST',
        url: urlGoogleAuth,
        data: usuario,
        dataType: "text"
    });
    request.done(function (json) {
        console.log(json);
        location.reload();
    });
}