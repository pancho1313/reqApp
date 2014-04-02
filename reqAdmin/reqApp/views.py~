from django.shortcuts import render
from reqApp.forms import *
from reqApp.util import *

from django.contrib.auth.models import User

def elementView(request, mensajes, modelFormClass, formTemplate, modelClass, listaAtributos, navbar):
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
        'navbar':navbar,
    }
    return render(request, 'reqApp/lista_expandible.html', context)

def viewTU(request):
    mensajes = []
    
    listaAtributos = [
        {'orden': 'identificador', 'posicion': 15,},
        {'orden': 'nombre', 'posicion': 9,},
    ]
    
    navbar = {'1':'proyecto', '2':'TU'}
    
    return elementView(request, mensajes, TUForm, 'reqApp/TU_form.html', TipoUsuario, listaAtributos, navbar)

def viewRU(request):
    mensajes = []
    
    listaAtributos = [
        {'orden': 'identificador', 'posicion': 15,},
        {'orden': 'nombre', 'posicion': 9,},
        {'orden': 'estado', 'posicion': 13,},
        {'orden': 'costo', 'posicion': 6,},
        {'orden': 'prioridad', 'posicion': 13,},
        {'orden': 'tipo', 'posicion': 18,},
        {'orden': 'hito', 'posicion': 10,},
    ]    
    
    navbar = {'1':'proyecto', '2':'RU'}
    
    return elementView(request, mensajes, RUForm, 'reqApp/RU_form.html', RequisitoUsuario, listaAtributos, navbar)

def viewRS(request):
    mensajes = []
    
    listaAtributos = [
        {'orden': 'identificador', 'posicion': 15,},
        {'orden': 'nombre', 'posicion': 9,},
        {'orden': 'estado', 'posicion': 13,},
        {'orden': 'costo', 'posicion': 6,},
        {'orden': 'prioridad', 'posicion': 13,},
        {'orden': 'tipo', 'posicion': 18,},
        {'orden': 'hito', 'posicion': 10,},
    ]  
    
    navbar = {'1':'proyecto', '2':'RS'}
    
    return elementView(request, mensajes, RSForm, 'reqApp/RS_form.html', RequisitoSoftware, listaAtributos, navbar)

def viewMD(request):
    mensajes = []
    
    listaAtributos = [
        {'orden': 'identificador', 'posicion': 15,},
        {'orden': 'nombre', 'posicion': 41,},
        {'orden': 'costo', 'posicion': 8,},
        {'orden': 'prioridad', 'posicion': 10,},
    ]
    
    navbar = {'1':'proyecto', '2':'MD'}
    
    return elementView(request, mensajes, MDForm, 'reqApp/MD_form.html', Modulo, listaAtributos, navbar)

def viewCP(request):
    mensajes = []    
    
    listaAtributos = [
        {'orden': 'identificador', 'posicion': 15,},
        {'orden': 'nombre', 'posicion': 9,},
        {'orden': 'estado', 'posicion': 20,},
        {'orden': 'requisito', 'posicion': 10,},
    ]
    
    navbar = {'1':'proyecto', '2':'CP'}
    
    return elementView(request, mensajes, CPForm, 'reqApp/CP_form.html', CasoPrueba, listaAtributos, navbar)
    
def viewHT(request):
    mensajes = []    
    
    listaAtributos = [
        {'orden': 'identificador', 'posicion': 15,},
        {'orden': 'nombre', 'posicion': 9,},
    ]
    
    navbar = {'1':'proyecto', '2':'HT'}
    
    return elementView(request, mensajes, HTForm, 'reqApp/HT_form.html', Hito, listaAtributos, navbar)
