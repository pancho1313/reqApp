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
function validForm(form){
    $.ajax({
        url: "",
        data: form.serialize() + "&solo_validar=1",
        type: "POST",
        success: function(data){
            if(data.server_response == "OK"){
                alert(data.server_response);
                form.submit();
            }else{
                // TODO: recorrer el diccionario (key=input_name,val=error_message),
                // pintar de rojo inputs con errores y mostrar los mensajes de error de cada input en un div de errores del formulario?
                alert(data.server_response);
            }
       }
    });
}
