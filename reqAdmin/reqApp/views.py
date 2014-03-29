from django.shortcuts import render
from reqApp.forms import *
from reqApp.util import *

from django.contrib.auth.models import User

def elementView(request, mensajes, modelFormClass, formTemplate, modelClass):
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
        """  
        context = {
            'mensajes': mensajes,
            'form_template': 'reqApp/element_form.html',
            'form': modelFormClass().asignarProyecto(proyecto),
            'borrar_form': 'reqApp/delete_element_form.html',
        }
        """
        
    #elif request.method == 'GET':
    listaElementos = []
    elementos = modelClass.objects.vigentes(proyecto)#TODO orderBy
    for elemento in elementos:
        listaElementos.append({'elemento':elemento, 'template':elemento.htmlTemplate(), 'form':modelFormClass(instance=elemento).asignarProyecto(elemento.proyecto)})
    context = {
        'mensajes': mensajes,
        'elementos': listaElementos,
        'form': modelFormClass().asignarProyecto(proyecto),
        'form_template': formTemplate,
        'borrar_form': 'reqApp/delete_element_form.html',
    }
    return render(request, 'reqApp/lista_expandible.html', context)

def viewTU(request):
    mensajes = ['holi soy TU',]    
    return elementView(request, mensajes, TUForm, 'reqApp/TU_form.html', TipoUsuario)

def viewRU(request):
    mensajes = ['holi soy RU',]    
    return elementView(request, mensajes, RUForm, 'reqApp/RU_form.html', RequisitoUsuario)

def viewRS(request):
    mensajes = ['holi soy RS',]    
    return elementView(request, mensajes, RSForm, 'reqApp/RS_form.html', RequisitoSoftware)

def viewMD(request):
    mensajes = ['holi soy MD',]    
    return elementView(request, mensajes, MDForm, 'reqApp/MD_form.html', Modulo)

def viewCP(request):
    mensajes = ['holi soy CP',]    
    return elementView(request, mensajes, CPForm, 'reqApp/CP_form.html', CasoPrueba)
