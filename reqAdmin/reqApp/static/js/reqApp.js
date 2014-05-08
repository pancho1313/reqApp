// -*- encoding: utf-8 -*-
// para expandir y contraer elementos
function expandirContraerElemento(id){
    var elemento_contenido = document.getElementById(id);
    elemento_contenido.style.display = (elemento_contenido.style.display == 'block') ? 'none' : 'block';
}

// ocultar formulario de edición y volver a mostrar el elemento de lista
function cancelarEdicionElemento(id){
    var elemento_form = document.getElementById(id+"_form");
    var elemento = document.getElementById(id);
    elemento_form.style.display = 'none';
    elemento.style.display = 'block';
}

// ocultar el elemento de lista y mostrar el formulario de edición
function editarElemento(id){
    var elemento_form = document.getElementById(id+"_form");
    var elemento = document.getElementById(id);
    elemento_form.style.display = 'block';
    elemento.style.display = 'none';
}

// ocultar edicion de nuevo elemento de lista
function cancelarNuevoElemento(){
    var elemento = document.getElementById('nuevoElemento');
    elemento.style.display = 'none';
}

// mostrar edicion de un nuevo elemento de lista
function editarNuevoElemento(){
    var elemento = document.getElementById('nuevoElemento');
    elemento.style.display = 'block';
}

// borrar un elemento de lista
function borrarElemento(identificador, csrf){
    // confirmar accion
    if(!confirm("¿Desea eliminarlo de la lista?"))
        return;

    var params = new Array();
    params["csrfmiddlewaretoken"] = csrf;// '{{csrf_token}}'
    params["identificador"] = identificador;
    params["borrar"] = "borrar";
    
    post_to_url("", params, "post");
}

// abrir la descripcion de todos los elementos de lista
function abrirTodos(){
    var elementos = document.getElementsByName('elemento_contenido');
    for(var i = 0; i < elementos.length; i++){
        elementos[i].style.display = 'block';
    }
}

// cerrar la descripcion de todos los elementos de lista
function cerrarTodos(){
    var elementos = document.getElementsByName('elemento_contenido');
    for(var i = 0; i < elementos.length; i++){
        elementos[i].style.display = 'none';
    }
}

// mostrar elementos de fila y columna seleccionada en la matriz de trazado
function mostrarElementosDeMatrizDeTrazado(elFila, elFilaEstado, elCol, elColEstado){
    document.getElementById('fila').innerHTML = "<div class="+elFilaEstado+">"+elFila+"</div>";
    document.getElementById('columna').innerHTML = "<div href='#' class="+elColEstado+">"+elCol+"</div>";
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


/* para probar la adicion de imagenes a tinymce */
function addImgExperimental(src){
    var /*f = document.forms[0], nl = f.elements,*/ ed = tinymce.EditorManager.activeEditor, args = {}, el;

	//tinyMCEPopup.restoreSelection(); // IE fix boo!

	if (src === '') {
		if (ed.selection.getNode().nodeName == 'IMG') {
			ed.dom.remove(ed.selection.getNode());
			ed.execCommand('mceRepaint');
		}

		//tinyMCEPopup.close();
		return;
	}

	if (!ed.settings.inline_styles) {
		args = tinymce.extend(args, {
			//vspace : nl.vspace.value,
			//hspace : nl.hspace.value,
			//border : nl.border.value,
			//align : getSelectValue(f, 'align')
		});
	} else
		args.style = this.styleVal;

	tinymce.extend(args, {
		src : src.replace(/ /g, '%20'),
		//alt : f.alt.value,
		//width : f.width.value,
		//height : f.height.value
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

	//tinyMCEPopup.close();
}

// ajax para insertar img en mce
function insertMceImg(input,url,csrf){

    //event = event || window.event; // cross browser
    //event.preventDefault(); // para evitar recargar la pagina completa
    
    var file = input.files[0];//$('#imgUp')[0].files[0];
    var fd = new FormData();		        
    fd.append('file', file);
    fd.append('csrfmiddlewaretoken', csrf);
    
    $.ajax({
        url: url,//"/upload/image/",
        data: fd,
        type: "POST",
        cache: false,
	    contentType: false,
	    processData: false,
        success: function(data){
            if(data != ""){
                alert(data);
            }else{
                alert('error');
            }
       }
    });
    
    // evitar que se recargue la pagina
    return false;	
}
