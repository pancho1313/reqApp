from django.shortcuts import render
from reqApp.forms import *
from reqApp.util import *

from django.contrib.auth.models import User

def elementView(request, mensajes, modelFormClass):
    usuario = User.objects.get(username='alejandro') #TODO#get_user_or_none(request)
    proyecto = proyectoDeUsuario(usuario)
    if request.method == 'POST':
        form = modelFormClass(request.POST)
        if form.is_valid():
            mensajes.append('form valid!')
            if 'identificador' in request.POST:
                identificador = request.POST['identificador']
                mensajes.append('vas a editar! identificador=' + identificador)
            else:
                form.asignarProyecto(proyecto)
                form.crearElementoDeBitacora(usuario)
                mensajes.append('saved form!')
        else:
            mensajes.append('invalid form!')
    
    context = {
        'mensajes': mensajes,
        'form_template': 'reqApp/element_form.html',
        'form': modelFormClass().asignarProyecto(proyecto),
    }
    return render(request, 'reqApp/lista_expandible.html', context)

def viewTU(request):
    mensajes = ['holi soy TU',]    
    return elementView(request, mensajes, TUForm)
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
    return elementView(request, mensajes, RUForm)

def viewRS(request):
    mensajes = ['holi soy RS',]    
    return elementView(request, mensajes, RSForm)

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
