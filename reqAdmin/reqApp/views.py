from django.shortcuts import render
from reqApp.forms import *
from reqApp.util import *

from django.contrib.auth.models import User

def elementView(request, mensajes, modelFormClass, modelClass):
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
    
        context = {
            'mensajes': mensajes,
            'form_template': 'reqApp/element_form.html',
            'form': modelFormClass().asignarProyecto(proyecto),
            'borrar_form': 'reqApp/delete_element_form.html',
        }
        
    elif request.method == 'GET':
        listaElementos = []
        elementos = modelClass.objects.vigentes(proyecto)#TODO orderBy
        for elemento in elementos:
            listaElementos.append({'elemento':elemento, 'form':modelFormClass(instance=elemento).asignarProyecto(elemento.proyecto)})
        context = {
            'mensajes': mensajes,
            'elementos': listaElementos,
            'elemento_template': 'reqApp/elemento.html',
            'form': modelFormClass().asignarProyecto(proyecto),
            'form_template': 'reqApp/element_form.html',
            'borrar_form': 'reqApp/delete_element_form.html',
        }
    return render(request, 'reqApp/lista_expandible.html', context)

def viewTU(request):
    mensajes = ['holi soy TU',]    
    return elementView(request, mensajes, TUForm, TipoUsuario)
    """
    if request.method == 'POST':
        form = TUForm(request.POST)
        if form.is_valid():
            mensajes.append('form valid!')
            if 'identificador' in request.POST:
                identificador = request.POST['identificador']
                mensajes.append('vas a editar! identificador=' + identificador)
            else:
                usuario = User.objects.get(username='alejandro') #TODO#get_user_or_none(request)
                form.crearElementoDeBitacora(usuario)
                mensajes.append('saved form!')
        else:
            mensajes.append('invalid form!')
    
    context = {
        'mensajes': mensajes,
        'form_template': 'reqApp/element_form.html',
        'form': TUForm(),
    }
    return render(request, 'reqApp/lista_expandible.html', context)
    """

def viewRU(request):
    mensajes = ['holi soy RU',]    
    return elementView(request, mensajes, RUForm, RequisitoUsuario)

def viewRS(request):
    mensajes = ['holi soy RS',]    
    return elementView(request, mensajes, RSForm, RequisitoSoftware)

def viewMD(request):
    elementosDeLista = [
    "MD1","MD2","MD3",
    ]
    context = {'elementos_de_lista': elementosDeLista}
    return render(request, 'reqApp/lista_expandible.html', context)

def viewCP(request):
    elementosDeLista = [
    "CP1","CP2","CP3",
    ]
    context = {'elementos_de_lista': elementosDeLista}
    return render(request, 'reqApp/lista_expandible.html', context)
