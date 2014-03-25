from django.shortcuts import render
from reqApp.forms import *
from reqApp.util import *

from django.contrib.auth.models import User

def viewTU(request):
    mensajes = ['holi soy TU',]    
    
    if request.method == 'POST':
        form = TUForm(request.POST)
        if form.is_valid():
            mensajes.append('form valid!')
            
            usuario = User.objects.get(username='alejandro') #TODO#get_user_or_none(request)
            form.crearElementoDeBitacora(usuario)
            mensajes.append('saved form!')
        else:
            mensajes.append('invalid form!')
    
    context = {
        'mensajes': mensajes,
        'form_template': 'reqApp/TU_form.html',
        'form': TUForm(),
    }
    return render(request, 'reqApp/lista_expandible.html', context)

def viewRU(request):
    elementosDeLista = [
    "RU1","RU2","RU3",
    ]
    context = {'elementos_de_lista': elementosDeLista}
    return render(request, 'reqApp/lista_expandible.html', context)

def viewRS(request):
    elementosDeLista = [
    "RS1","RS2","RS3",
    ]
    context = {'elementos_de_lista': elementosDeLista}
    return render(request, 'reqApp/lista_expandible.html', context)

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
