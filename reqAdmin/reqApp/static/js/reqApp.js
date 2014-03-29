# -*- encoding: utf-8 -*-
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

// mostrar el selector de requisitos asociados a un CP según el tipo (RU ó RS), y limpiar la info. del inactivo
function seleccionarRequisitoCP(selecRU){
    var ru = document.getElementById("id_requisitoUsuario");
    var rs = document.getElementById("id_requisitoSoftware");
    var _ru = document.getElementById("_id_requisitoUsuario");
    var _rs = document.getElementById("_id_requisitoSoftware");
    
    if(selecRU){
        alert("ru");
        _ru.style.display = 'block';
        _rs.style.display = 'none';
    }else{
        alert("rs");
        _ru.style.display = 'none';
        _rs.style.display = 'block';
    }
}
