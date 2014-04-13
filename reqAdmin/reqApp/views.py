# -*- encoding: utf-8 -*-
from django.shortcuts import render
from reqApp.forms import *
from reqApp.util import *
from django.contrib.auth.models import User

################ Proyecto ################

def elementView(request, mensajes, modelFormClass, formTemplate, modelClass, listaAtributos, navbar):
    usuario = User.objects.get(username='alejandro') #TODO#get_user_or_none(request)
    proyecto = proyectoDeUsuario(usuario)
    if request.method == 'POST':
        if 'identificador' in request.POST:# editar o borrar
            identificador = request.POST['identificador']
            instance = modelClass.objects.vigente(proyecto, identificador)
            if 'borrar' in request.POST:# borrar elemento
                instance.bitacorarElementoBorrado(usuario)
                mensajes.append('elemento borrado!')
            else:# editar elemento
                form = modelFormClass(instance=instance, data=request.POST)
                if form.is_valid():
                    form.asignarProyecto(proyecto)
                    form.actualizarElementoDeBitacora(usuario, identificador)
                    mensajes.append('elemento editado!')
                else:
                    mensajes.append('datos inválidos!')
        else:# crear
            form = modelFormClass(request.POST)
            if form.is_valid():
                form.asignarProyecto(proyecto)
                form.crearElementoDeBitacora(usuario)
                mensajes.append('elemento creado!')
            else:
                mensajes.append('datos inválidos!')
    
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
    
    return elementView(request, mensajes, TUForm, 'reqApp/proyecto/TU/TU_form.html', TipoUsuario, listaAtributos, navbar)

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
    
    return elementView(request, mensajes, RUForm, 'reqApp/proyecto/RU/RU_form.html', RequisitoUsuario, listaAtributos, navbar)

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
    
    return elementView(request, mensajes, RSForm, 'reqApp/proyecto/RS/RS_form.html', RequisitoSoftware, listaAtributos, navbar)

def viewMD(request):
    mensajes = []
    
    listaAtributos = [
        {'orden': 'identificador', 'posicion': 15,},
        {'orden': 'nombre', 'posicion': 41,},
        {'orden': 'costo', 'posicion': 8,},
        {'orden': 'prioridad', 'posicion': 10,},
    ]
    
    navbar = {'1':'proyecto', '2':'MD'}
    
    return elementView(request, mensajes, MDForm, 'reqApp/proyecto/MD/MD_form.html', Modulo, listaAtributos, navbar)

def viewCP(request):
    mensajes = []    
    
    listaAtributos = [
        {'orden': 'identificador', 'posicion': 15,},
        {'orden': 'nombre', 'posicion': 9,},
        {'orden': 'estado', 'posicion': 20,},
        {'orden': 'requisito', 'posicion': 10,},
    ]
    
    navbar = {'1':'proyecto', '2':'CP'}
    
    return elementView(request, mensajes, CPForm, 'reqApp/proyecto/CP/CP_form.html', CasoPrueba, listaAtributos, navbar)
    
def viewHT(request):
    mensajes = []    
    
    listaAtributos = [
        {'orden': 'identificador', 'posicion': 15,},
        {'orden': 'nombre', 'posicion': 9,},
    ]
    
    navbar = {'1':'proyecto', '2':'HT'}
    
    return elementView(request, mensajes, HTForm, 'reqApp/proyecto/HT/HT_form.html', Hito, listaAtributos, navbar)
    
################################# Documentos #############################
def docView(request, navbar):
    context = {
        'navbar':navbar,
    }
    return render(request, 'reqApp/documentos.html', context)

def docRequisitos(request):
    navbar = {'1':'documentos', '2':'requisitos'}
    return docView(request, navbar)
    
def docDiseno(request):
    navbar = {'1':'documentos', '2':'diseno'}
    return docView(request, navbar)
    
def docCP(request):
    navbar = {'1':'documentos', '2':'cp'}
    return docView(request, navbar)

def docHistorico(request):
    navbar = {'1':'documentos', '2':'historico'}
    return docView(request, navbar)

############################### Herramientas ##########################
def HerrView(request, navbar):
    context = {
        'navbar':navbar,
    }
    return render(request, 'reqApp/herramientas.html', context)

def tareas(request):
    navbar = {'1':'herramientas', '2':'tareas'}
    return HerrView(request, navbar)
    
def estadisticas(request):
    navbar = {'1':'herramientas', '2':'estadisticas'}
    return HerrView(request, navbar)
    
def matrices(request):
    MATRIZ_CHOICES = [
        ("rurs", "RU/RS"),
        ("mdrs", "MD/RS"),
        ("rucp", "RU/CP"),
        ("rscp", "RS/CP"),
    ]

    usuario = User.objects.get(username='alejandro') #TODO#get_user_or_none(request)
    proyecto = proyectoDeUsuario(usuario)
    navbar = {'1':'herramientas', '2':'matrices'}
    
    tipo =  request.GET.get('tipo', 'rurs')
    
    if tipo == 'rurs':
        model1 = RequisitoUsuario
        model2 = RequisitoSoftware
    elif tipo == 'mdrs':
        model1 = Modulo
        model2 = RequisitoSoftware
    elif tipo == 'rucp':
        model1 = RequisitoUsuario
        model2 = CasoPrueba
    elif tipo == 'rscp':
        model1 = RequisitoSoftware
        model2 = CasoPrueba
    
    m1s = model1.objects.vigentes(proyecto)
    m2s = model2.objects.vigentes(proyecto)
    filas = []
    for fila in range(0,len(m1s)):
        filas.append([])
        for col in range(0,len(m2s)):
            match = m1s[fila].matrixMatch(proyecto, m2s[col])
            filas[fila].append({
                'fila':m1s[fila],
                'col':m2s[col],
                'match':match,
                })
    
    context = {
        'navbar':navbar,
        'filas':filas,
        'MATRIZ_CHOICES':MATRIZ_CHOICES,
        'tipo':tipo,
    }
    return render(request, 'reqApp/herramientas/matrices/matrices.html', context)
    
def consistencia(request):
    navbar = {'1':'herramientas', '2':'consistencia'}
    return HerrView(request, navbar)
    
def bitacora(request):
    navbar = {'1':'herramientas', '2':'bitacora'}
    return HerrView(request, navbar)
