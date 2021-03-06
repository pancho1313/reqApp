// -*- encoding: utf-8 -*-
// para expandir y contraer elementos
function expandirContraerElemento(id){
    var elemento = $('#'+id);
    if(elemento.css('display') == 'block'){
        elemento.hide('slow');
    }else{
        elemento.show('slow');
    }
}

// para expandir y contraer el contenido de los elementos de lista
function expandirContraerContenido(self){
    var elemento_contenido = $(self).parent().parent().parent().next('div[name=elemento_contenido]');
    if(elemento_contenido.css('display') == 'block'){
        elemento_contenido.hide('slow');
    }else{
        elemento_contenido.show('slow');
    }
}

// ocultar formulario de edición y volver a mostrar el elemento de lista
function cancelarEdicionElemento(id){
    //location.reload(true); // problemas con reenvio de formularios
    window.location = window.location.href.split("#")[0];
}

// ocultar el elemento de lista y mostrar el formulario de edición
function editarElemento(id){
    $('#'+id+'_form').show('slow');
    $('#'+id).hide('slow');
}

// ocultar edicion de nuevo elemento de lista
function cancelarNuevoElemento(){
    //location.reload(true); // problemas con reenvio de formularios
    window.location = window.location.href.split("#")[0];
}

// mostrar edicion de un nuevo elemento de lista
function editarNuevoElemento(){
    $('#nuevoElemento').show();
}

// borrar un elemento de lista
function borrarElemento(textoId, identificador, csrf){
    // confirmar accion
    if(!confirm("¿Desea eliminar "+textoId+" de la lista?"))
        return;

    var params = new Array();
    params["csrfmiddlewaretoken"] = csrf;// '{{csrf_token}}'
    params["identificador"] = identificador;
    params["borrar"] = "borrar";
    
    post_to_url("", params, "post");
}

// abrir la descripcion de todos los elementos de lista
function abrirTodos(){
    var elementos = $('[name=elemento_contenido]');
    elementos.show('slow');
}

// cerrar la descripcion de todos los elementos de lista
function cerrarTodos(){
    var elementos = $('[name=elemento_contenido]');
    elementos.hide('slow');
}

// ajax para verificacion de formularios
function validForm(event,button){
    var form = button.form;
    button.disabled = true; // deshabilitar el boton submit

    event = event || window.event; // cross browser
    event.preventDefault(); // para evitar recargar la pagina completa

    // agregar marca al post ajax
    var input = document.createElement("input");
    input.type = "hidden";
    input.name = "solo_validar";
    input.value = '1';
    form.appendChild(input);
    
    $.ajax({
        url: "",
        data: $(form).serialize(),
        type: "POST",
        success: function(data){
            if(data.server_response == "OK"){
                // remover marca ajax
                form.removeChild(input);
                
                // enviar formulario
                form.submit();
            }else{
                // remover marca ajax
                form.removeChild(input);
                button.disabled = false;// habilitar el boton submit para corregir errores
                // mostrar errores
                for(var e = 0; e < data.errores.length; e++){
                    input_name = data.errores[e][0];
                    input_error = data.errores[e][1];
                    var campo = form.elements[input_name];
                    if(campo!=undefined){
                        campo.className += " invalido";
                        var newInput = $("<div style='color:Red'>"+input_error+"</div>");
                        $(campo).before(newInput);
                    }
                }
            }
       }
    });
    
    // evitar que se recargue la pagina
    return false;
}

// js create & send post form
function post_to_url(path, params, method) {
    //var params = new Array(); params["file"] = 'test.pdf';
    method = method || "post"; // Set method to post by default if not specified.

    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);

    for(var key in params) {
        if(params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
         }
    }

    document.body.appendChild(form);
    form.submit();
}


/* adicion de imagenes a tinymce */
function addMCEImg(src){
    var ed = tinymce.EditorManager.activeEditor, args = {}, el;

	if (src === '') {
		if (ed.selection.getNode().nodeName == 'IMG') {
			ed.dom.remove(ed.selection.getNode());
			ed.execCommand('mceRepaint');
		}
		return;
	}

	if (!ed.settings.inline_styles) {
		args = tinymce.extend(args, {
		});
	} else
		args.style = this.styleVal;

	tinymce.extend(args, {
		src : src.replace(/ /g, '%20'),
		//'data-mce-src' : pre_src + src.replace(/ /g, '%20'), // hack to avoid src-replace after save-mce
		alt : "ERROR_IMG_NOT_FOUND: " + src.replace(/ /g, '%20'),
		//width : 100, // set default size??
		//height : 100 // set default size??
	});

	el = ed.selection.getNode();

	if (el && el.nodeName == 'IMG') {
		ed.dom.setAttribs(el, args);
		ed.execCommand('mceRepaint');
		ed.focus();
	} else {
		tinymce.each(args, function(value, name) {
			if (value === "") {
				delete args[name];
			}
		});

		ed.execCommand('mceInsertContent', false, ed.dom.createHTML('img', args), {skip_undo : 1});
		ed.undoManager.add();
	}
}

// ajax para insertar img en mce
function insertMceImg(input,url,csrf,host){
    var file = input.files[0];
    var fd = new FormData();		        
    fd.append('file', file);
    fd.append('csrfmiddlewaretoken', csrf);
    
    $.ajax({
        url: url,
        data: fd,
        type: "POST",
        cache: false,
	    contentType: false,
	    processData: false,
        success: function(data){
            if(data != ""){
                addMCEImg(data, host);//"http://localhost:8000");
            }else{
                alert('ERROR: archivo de imagen inválido!');
            }
       }
    });
}

//prompt para añadir img al mce por su url
function promptImgURL(){
    var url = prompt("Insert Image By URL:", "http://anakena.dcc.uchile.cl/anakena.jpg");
    if (url!=null) {
        addMCEImg(url);
    }
}
