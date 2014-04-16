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
    document.getElementById('fila').innerHTML = "<b class="+elFilaEstado+">"+elFila+"</b>";
    document.getElementById('columna').innerHTML = "<b href='#' class="+elColEstado+">"+elCol+"</b>";
}

// ajax para verificacion de formularios
function validForm(event,button){
    // TODO: agregar confirm box (OK, Cancelar)?
    var form = button.form;
    button.disabled = true; // deshabilitar el boton submit

    event = event || window.event // cross browser
    event.preventDefault(); // para evitar recargar la pagina completa

    // agregar marca al post ajax
    var input = document.createElement("input");
    input.type = "hidden";
    input.name = "solo_validar";
    input.value = "1";
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
                // TODO: recorrer el diccionario (key=input_name,val=error_message),
                // pintar de rojo inputs con errores y mostrar los mensajes de error de cada input en un div de errores del formulario?
                alert(data.server_response);
                button.disabled = false;// habilitar el boton submit para corregir errores
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
