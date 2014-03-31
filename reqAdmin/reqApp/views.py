from django.shortcuts import render
from reqApp.forms import *
from reqApp.util import *

from django.contrib.auth.models import User

def elementView(request, mensajes, modelFormClass, formTemplate, modelClass, listaAtributos):
    usuario = User.objects.get(username='alejandro') #TODO#get_user_or_none(request)
    proyecto = proyectoDeUsuario(usuario)
    if request.method == 'POST':
        if 'identificador' in request.POST:# editar o borrar
            identificador = request.POST['identificador']
            instance = modelClass.objects.vigente(proyecto, identificador)
            if 'borrar' in request.POST:# borrar elemento
                mensajes.append('vas a borrar! identificador=' + identificador)
                instance.bitacorarElementoBorrado(usuario)
                mensajes.append('borrado!')
            else:# editar elemento
                mensajes.append('vas a editar! identificador=' + identificador)
                form = modelFormClass(instance=instance, data=request.POST)
                if form.is_valid():
                    form.asignarProyecto(proyecto)
                    form.actualizarElementoDeBitacora(usuario, identificador)
                    mensajes.append('saved form!')
                else:
                    mensajes.append('invalid form!')
        else:# crear
            mensajes.append('vas a crear!')
            form = modelFormClass(request.POST)
            if form.is_valid():
                form.asignarProyecto(proyecto)
                form.crearElementoDeBitacora(usuario)
                mensajes.append('saved form!')
            else:
                mensajes.append('invalid form!')
    
    ordenActual = 'identificador'
    if 'orden' in request.GET:# ordenar lista de elementos
        ordenActual = request.GET['orden']
        elementos = modelClass.objects.vigentes(proyecto, ordenActual)
    else:
        elementos = modelClass.objects.vigentes(proyecto)
    
    listaElementos = []
    for elemento in elementos:
        listaElementos.append({'elemento':elemento, 'template':elemento.htmlTemplate(), 'form':modelFormClass(instance=elemento).asignarProyecto(elemento.proyecto)})
    
    context = {
        'mensajes': mensajes,
        'elementos': listaElementos,
        'form': modelFormClass().asignarProyecto(proyecto),
        'form_template': formTemplate,
        'borrar_form': 'reqApp/delete_element_form.html',
        'barra_orden_elementos': 'reqApp/orden_elementos.html',
        'atributos_ordenables': listaAtributos,
        'orden_actual': ordenActual,
    }
    return render(request, 'reqApp/lista_expandible.html', context)

def viewTU(request):
    mensajes = []
    
    listaAtributos = [
        {'orden': 'identificador', 'porcentaje': 15,},
        {'orden': 'nombre', 'porcentaje': 9,},
    ]
      
    return elementView(request, mensajes, TUForm, 'reqApp/TU_form.html', TipoUsuario, listaAtributos)

def viewRU(request):
    mensajes = []
    
    listaAtributos = [
        {'orden': 'identificador', 'porcentaje': 15,},
        {'orden': 'nombre', 'porcentaje': 9,},
        {'orden': 'estado', 'porcentaje': 13,},
        {'orden': 'costo', 'porcentaje': 6,},
        {'orden': 'prioridad', 'porcentaje': 13,},
        {'orden': 'tipo', 'porcentaje': 18,},
        {'orden': 'hito', 'porcentaje': 10,},
    ]    
    
    return elementView(request, mensajes, RUForm, 'reqApp/RU_form.html', RequisitoUsuario, listaAtributos)

def viewRS(request):
    mensajes = []
    
    listaAtributos = [
        {'orden': 'identificador', 'porcentaje': 15,},
        {'orden': 'nombre', 'porcentaje': 9,},
        {'orden': 'estado', 'porcentaje': 13,},
        {'orden': 'costo', 'porcentaje': 6,},
        {'orden': 'prioridad', 'porcentaje': 13,},
        {'orden': 'tipo', 'porcentaje': 18,},
        {'orden': 'hito', 'porcentaje': 10,},
    ]  
     
    return elementView(request, mensajes, RSForm, 'reqApp/RS_form.html', RequisitoSoftware, listaAtributos)

def viewMD(request):
    mensajes = []
    
    listaAtributos = [
        {'orden': 'identificador', 'porcentaje': 15,},
        {'orden': 'nombre', 'porcentaje': 41,},
        {'orden': 'costo', 'porcentaje': 8,},
        {'orden': 'prioridad', 'porcentaje': 10,},
    ]
       
    return elementView(request, mensajes, MDForm, 'reqApp/MD_form.html', Modulo, listaAtributos)

def viewCP(request):
    mensajes = []    
    
    listaAtributos = [
        {'orden': 'identificador', 'porcentaje': 15,},
        {'orden': 'nombre', 'porcentaje': 9,},
        {'orden': 'estado', 'porcentaje': 20,},
        {'orden': 'requisito', 'porcentaje': 10,},
    ]
    
    return elementView(request, mensajes, CPForm, 'reqApp/CP_form.html', CasoPrueba, listaAtributos)
