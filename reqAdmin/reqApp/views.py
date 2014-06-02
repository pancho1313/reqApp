# -*- encoding: utf-8 -*-
from django.shortcuts import render
from reqApp.forms import *
from reqApp.util import *
from django.contrib.auth.models import User
#from django.utils import simplejson
import json

from django.http import HttpResponse
from django.http import Http404

from django.db.models import Sum

################ Proyecto ################

def ajax_form_valid(form, validado):
    # para validar a traves de ajax
    if validado:
        response_dict = {'server_response': "OK" }
        return HttpResponse(json.dumps(response_dict), content_type='application/json')    
    else:
        errores = []
        for campo, errors in form.errors.items():
            for error in errors:
                errores.append([campo,error])
        response_dict = {'server_response': "FAIL", 'errores':errores}
        return HttpResponse(json.dumps(response_dict), content_type='application/json')

def elementView(request, mensajes, modelFormClass, elementTemplate, formTemplate, modelClass, listaAtributos, navbar, pdfLink=None):
    usuario = get_user_or_none(request) # TODO is None?
    proyecto = proyectoDeUsuario(usuario)
    if request.method == 'POST':
        if 'identificador' in request.POST:# editar o borrar
            identificador = request.POST['identificador']
            instance = modelClass.objects.vigente(proyecto, identificador)
            if 'borrar' in request.POST:# borrar elemento
                instance.bitacorarElementoBorrado(usuario)
                mensajes.append('elemento borrado y registrado en la bitácora')
            else:# editar elemento
                form = modelFormClass(instance=instance, data=request.POST)
                if form.is_valid():
                    if request.POST.has_key("solo_validar"):
                        return ajax_form_valid(form, True)
                    form.asignarProyecto(proyecto)
                    form.actualizarElementoDeBitacora(usuario, identificador)
                    mensajes.append('elemento modificado y registrado en la bitácora')
                else:
                    if request.POST.has_key("solo_validar"):
                        return ajax_form_valid(form, False)
                    m=form.errors.as_text
                    mensajes.append('datos inválidos!')
                    mensajes.append(m)
        else:# crear
            form = modelFormClass(request.POST)
            if form.is_valid():
                if request.POST.has_key("solo_validar"):
                    return ajax_form_valid(form, True)
                form.asignarProyecto(proyecto)
                form.crearElementoDeBitacora(usuario)
                mensajes.append('elemento creado')
            else:
                if request.POST.has_key("solo_validar"):
                    return ajax_form_valid(form, False)
                mensajes.append('datos inválidos!')
    
    ordenActual = 'identificador'
    if 'orden' in request.GET:# ordenar lista de elementos
        ordenActual = request.GET['orden']
        elementos = modelClass.objects.vigentes(proyecto, ordenActual)
    else:
        elementos = modelClass.objects.vigentes(proyecto)
    
    listaElementos = []
    for elemento in elementos:
        listaElementos.append({'elemento':elemento, 'form':modelFormClass(instance=elemento).asignarProyecto(elemento.proyecto)})
    
    context = {
        'mensajes': mensajes,
        'elementos': listaElementos,
        'template':elementTemplate,
        'form': modelFormClass().asignarProyecto(proyecto),
        'form_template': formTemplate,# TODO: enviar solo si el usuario tiene permisos de edicion
        'barra_orden_elementos': 'reqApp/orden_elementos.html',
        'atributos_ordenables': listaAtributos,
        'orden_actual': ordenActual,
        'navbar':navbar,
        'pdfLink':pdfLink,
    }
    return render(request, 'reqApp/proyecto/lista_expandible.html', context)

def viewTU(request):
    mensajes = []
    
    # la 'posicion' corresponde al ancho(%) dentro del div (ver 'reqApp/orden_elementos.html')
    listaAtributos = [
        {'orden': 'identificador', 'posicion': 15,},
        {'orden': 'nombre', 'posicion': 9,},
    ]
    
    navbar = {'1':'proyecto', '2':'TU'}
    
    return elementView(request, mensajes, TUForm, 'reqApp/proyecto/TU/TU.html', 'reqApp/proyecto/TU/TU_form.html', TipoUsuario, listaAtributos, navbar, 'TU')

def viewRU(request):
    mensajes = []
    
    # la 'posicion' corresponde al ancho(%) dentro del div (ver 'reqApp/orden_elementos.html')
    listaAtributos = [
        {'orden': 'identificador', 'posicion': 15,},
        {'orden': 'nombre', 'posicion': 9,},
        {'orden': 'estado', 'posicion': 15,},
        {'orden': 'costo', 'posicion': 5,},
        {'orden': 'prioridad', 'posicion': 13,},
        {'orden': 'tipo', 'posicion': 18,},
        {'orden': 'hito', 'posicion': 10,},
    ]    
    
    navbar = {'1':'proyecto', '2':'RU'}
    
    return elementView(request, mensajes, RUForm, 'reqApp/proyecto/RU/RU.html', 'reqApp/proyecto/RU/RU_form.html', RequisitoUsuario, listaAtributos, navbar, 'RU')

def viewRS(request):
    mensajes = []
    
    # la 'posicion' corresponde al ancho(%) dentro del div (ver 'reqApp/orden_elementos.html')
    listaAtributos = [
        {'orden': 'identificador', 'posicion': 15,},
        {'orden': 'nombre', 'posicion': 9,},
        {'orden': 'estado', 'posicion': 15,},
        {'orden': 'costo', 'posicion': 5,},
        {'orden': 'prioridad', 'posicion': 13,},
        {'orden': 'tipo', 'posicion': 18,},
        {'orden': 'hito', 'posicion': 15,},
    ]  
    
    navbar = {'1':'proyecto', '2':'RS'}
    
    return elementView(request, mensajes, RSForm, 'reqApp/proyecto/RS/RS.html', 'reqApp/proyecto/RS/RS_form.html', RequisitoSoftware, listaAtributos, navbar, 'RS')

def viewMD(request):
    mensajes = []
    
    # la 'posicion' corresponde al ancho(%) dentro del div (ver 'reqApp/orden_elementos.html')
    listaAtributos = [
        {'orden': 'identificador', 'posicion': 15,},
        {'orden': 'nombre', 'posicion': 44,},
        {'orden': 'costo', 'posicion': 8,},
        {'orden': 'prioridad', 'posicion': 10,},
    ]
    
    navbar = {'1':'proyecto', '2':'MD'}
    
    return elementView(request, mensajes, MDForm, 'reqApp/proyecto/MD/MD.html', 'reqApp/proyecto/MD/MD_form.html', Modulo, listaAtributos, navbar, 'MD')

def viewCP(request):
    mensajes = []    
    
    # la 'posicion' corresponde al ancho(%) dentro del div (ver 'reqApp/orden_elementos.html')
    listaAtributos = [
        {'orden': 'identificador', 'posicion': 15,},
        {'orden': 'nombre', 'posicion': 9,},
        {'orden': 'estado', 'posicion': 20,},
        {'orden': 'requisito', 'posicion': 10,},
    ]
    
    navbar = {'1':'proyecto', '2':'CP'}
    
    return elementView(request, mensajes, CPForm, 'reqApp/proyecto/CP/CP.html', 'reqApp/proyecto/CP/CP_form.html', CasoPrueba, listaAtributos, navbar, 'CP')
    
def viewHT(request):
    mensajes = []    
    
    # la 'posicion' corresponde al ancho(%) dentro del div (ver 'reqApp/orden_elementos.html')
    listaAtributos = [
        {'orden': 'identificador', 'posicion': 15,},
        {'orden': 'nombre', 'posicion': 9,},
    ]
    
    navbar = {'1':'proyecto', '2':'HT'}
    
    return elementView(request, mensajes, HTForm, 'reqApp/proyecto/HT/HT.html', 'reqApp/proyecto/HT/HT_form.html', Hito, listaAtributos, navbar, 'HT')
    
################################# Documentos #############################
def docView(request, navbar, activos):
    usuario = get_user_or_none(request) # TODO is None?
    proyecto = proyectoDeUsuario(usuario)

    parrafo =  request.GET.get('parrafo', activos[0]) # valor por defecto si no corresponde a ningun tipo de parrafo conocido
    if parrafo not in activos:
        parrafo = activos[0]
        
    parrafos = []
    for pa in PARRAFOS_CHOICES:
        activo = False
        if pa[0] in activos:
            activo = True
        parrafos.append({'tipo':pa[0], 'nombre':pa[1], 'activo':activo})
    
    context = {
        'navbar':navbar,
        'parrafos':parrafos,
        'parrafo':parrafo,
    }
    
    id_version = -1 # sin version seleccionada para edición
    if request.method == 'POST':
        form = DocForm(request.POST)
        if form.is_valid():
            form.registrarDocumento(proyecto, usuario, parrafo) # guardar cambios
    elif request.method == 'GET':
        id_version =  int(request.GET.get('id', -1))# version seleccionada para edición
    
    versiones = Documento.objects.versiones(proyecto, parrafo, 10)# solo se muestran las ultimas 10 versiones de la sección/párrafo (<0 para mostrar todas)
    if len(versiones) > 0:
        vigente = versiones[0]
        context.update({'vigente':vigente,'versiones':versiones})
        
        if id_version >= 0: # si desea obtener una version en particular
            version = None
            for vers in versiones:
                if vers.id == id_version:
                    version = vers
                    break
                
            if version is not None: # si la version solicitada está presente en las versiones consideradas aquí
                form = DocForm(instance=version) # cargamos el editor mce con la versión solicitada
                context.update({'id_version':id_version})
            else: # si no se encontró la versión solocitada
                form = DocForm(instance=vigente) # se carga la versión actual (vigente)
        else:
            form = DocForm(instance=vigente) # se carga la versión actual (vigente)
    else:
        form = DocForm() # si no hay versiones registradas anteriormente para esta sección/párrafo
        
    context.update({'form':form,})
    
    #context.update({'host':request.build_absolute_uri("/")[:-1]})# http://localhost:8000 -->  reqApp/Documentos/mce.html --> static/js/reqApp.js/insertMceImg(input,url,csrf,host);
    
    return render(request, 'reqApp/documentos/documentos.html', context)

def docRequisitos(request):
    navbar = {'1':'documentos', '2':'requisitos'}
    parrafos = [
        'introduccion',
        'proposito',
        'alcance',
        'contexto',
        'definiciones',
        'referencias',
        'descripcion_general',
        
        'usuarios',
        'producto',
        'ambiente',
        'proyectos_relacionados',
    ]
    return docView(request, navbar, parrafos)
    
def docDiseno(request):
    navbar = {'1':'documentos', '2':'diseno'}
    parrafos = [
        'introduccion',
        'proposito',
        'alcance',
        'contexto',
        'definiciones',
        'referencias',
        'descripcion_general',
        
        'diseno',
        'arquitectura_fisica',
        'arquitectura_logica',
        'modelo',
        'detalle_modulos',
        'navegacion',
        'interfaz',
    ]
    return docView(request, navbar, parrafos)
    
def docCP(request):
    navbar = {'1':'documentos', '2':'cp'}
    parrafos = [
        'introduccion',
        'proposito',
        'alcance',
        'contexto',
        'definiciones',
        'referencias',
        'descripcion_general',
        
        'usuarios',
        'producto',
        'ambiente',
        'proyectos_relacionados',
    ]
    return docView(request, navbar, parrafos)

def docHistorico(request):
    navbar = {'1':'documentos', '2':'historico'}
    parrafos = [
        'introduccion',
        'proposito',
        'alcance',
        'contexto',
        'definiciones',
        'referencias',
        'descripcion_general',
        
        'usuarios',
        'producto',
        'ambiente',
        'proyectos_relacionados',
        
        'diseno',
        'arquitectura_fisica',
        'arquitectura_logica',
        'modelo',
        'detalle_modulos',
        'navegacion',
        'interfaz',
    ]
    return docView(request, navbar, parrafos)

############################### Herramientas ##########################
def herrView(request, navbar):
    context = {
        'navbar':navbar,
    }
    return render(request, 'reqApp/herramientas.html', context)

##############################  TAREAS
def tareas(request):
    navbar = {'1':'herramientas', '2':'tareas'}
    return herrView(request, navbar)

##############################  ESTADISTICAS
def myFilter(s,val):
    # para la generacion de tablas (estadisticas)
    dic = {}
    dic[s] = val
    return dic
def estadisticas(request):
    HT_CHOICES = [
        (0, "Todos"),
    ]

    usuario = get_user_or_none(request) # TODO is None?
    proyecto = proyectoDeUsuario(usuario)
    navbar = {'1':'herramientas', '2':'estadisticas'}
    
    if request.method == 'GET':
        hito = int(request.GET.get('hito', 0))
        hitos = Hito.objects.vigentes(proyecto)
        for ht in hitos:
            HT_CHOICES.append((ht.identificador,ht.nombre))
        if hito > 0:
            ht = hitos.get(identificador=hito)
        
        # estadisticas de requisitos de usuario
        q = RequisitoUsuario.objects.vigentes(proyecto).filter(hito__vigencia=True)
        if hito > 0:
            q = q.filter(hito=ht)
        ru = {}
        prioridad = []
        estabilidad = []
        tipo = []
        estado = {}
        extras = []
        
        tabla = [
            ('Prioridad', 'prioridad', PRIORIDAD_CHOICES, prioridad),
            ('Estabilidad', 'estabilidad', ESTABILIDAD_CHOICES, estabilidad),
            ('Tipo', 'tipo', TIPO_RU_CHOICES, tipo),
        ]
        
        for atributo, s, choices, arreglo in tabla:
            dic = {'atributo':atributo,'atributos':len(choices)}
            for key, nombre in choices:
                dic.update({'nombre':nombre})
                qq = q.filter(**myFilter(s,key))
                total = 0
                for e, wanda in ESTADO_CHOICES:
                    c = qq.filter(estado=e).count()
                    dic.update({e:c})
                    total = total + c
                dic.update({'total':total})
                arreglo.append(dic)
                dic = {}
                     
        for e, nombre in ESTADO_CHOICES:
            qq = q.filter(estado=e)
            estado.update({e:qq.count()})
        
        total = q.count()
        extras.append({
            'nombre':'Sin RS asoc.',
            'cantidad':total - q.filter(requisitosoftware__vigencia=True).distinct().count()
        })
        extras.append({
            'nombre':'Sin TU asoc.',
            'cantidad':total - q.filter(tiposUsuario__vigencia=True).distinct().count()
        })
        extras.append({
            'nombre':'Costo total',
            'cantidad':q.aggregate(Sum('costo'))['costo__sum']
        })
        
        ru.update({'atributos':[prioridad,estabilidad,tipo]})
        ru.update({'estado':estado})
        ru.update({'extras':extras})
        ru.update({'total':total})
        
        # estadisticas de requisitos de software
        q = RequisitoSoftware.objects.vigentes(proyecto).filter(hito__vigencia=True)
        if hito > 0:
            q = q.filter(hito=ht)
        rs = {}
        prioridad = []
        estabilidad = []
        tipo = []
        estado = {}
        extras = []
        
        tabla = [
            ('prioridad', 'prioridad', PRIORIDAD_CHOICES, prioridad),
            ('estabilidad', 'estabilidad', ESTABILIDAD_CHOICES, estabilidad),
            ('tipo', 'tipo', TIPO_RS_CHOICES, tipo),
        ]
        
        for atributo, s, choices, arreglo in tabla:
            dic = {'atributo':atributo,'atributos':len(choices)}
            for key, nombre in choices:
                dic.update({'nombre':nombre})
                qq = q.filter(**myFilter(s,key))
                total = 0
                for e, wanda in ESTADO_CHOICES:
                    c = qq.filter(estado=e).count()
                    dic.update({e:c})
                    total = total + c
                dic.update({'total':total})
                arreglo.append(dic)
                dic = {}
                 
        for e, nombre in ESTADO_CHOICES:
            qq = q.filter(estado=e)
            estado.update({e:qq.count()})
        
        total = q.count()
        extras.append({
            'nombre':'Sin RU asoc.',
            'cantidad':total - q.filter(requisitosUsuario__vigencia=True).distinct().count()
        })
        extras.append({
            'nombre':'Sin TU asoc.',
            'cantidad':total - q.filter(tiposUsuario__vigencia=True).distinct().count()
        })
        costo = q.aggregate(Sum('costo'))['costo__sum']
        if costo == None:
            costo = 0
        extras.append({
            'nombre':'Costo total',
            'cantidad':costo
        })
        
        rs.update({'atributos':[prioridad,estabilidad,tipo]})
        rs.update({'estado':estado})
        rs.update({'extras':extras})
        rs.update({'total':total})
        
        # estadisticas de casos de prueba
        q = CasoPrueba.objects.vigentes(proyecto).filter(requisito__vigencia=True)
        q_ru = q.filter(requisito__requisitousuario__hito__vigencia=True)
        q_rs = q.filter(requisito__requisitosoftware__hito__vigencia=True)
        
        if hito > 0:
            q_ru = q_ru.filter(requisito__requisitousuario__hito=ht)
            q_rs = q_rs.filter(requisito__requisitosoftware__hito=ht)
        cp = {}
        tipo = []
        estado = {}
        extras = []
                 
        dic_asoc_RU = {'nombre':'asociados a RU','total':0}
        dic_asoc_RS = {'nombre':'asociados a RS','total':0}
        for e, wanda in ESTADO_CHOICES:
            casos_ru = q_ru.filter(estado=e).count()
            casos_rs = q_rs.filter(estado=e).count()
            
            dic_asoc_RU.update({e:casos_ru})
            dic_asoc_RU.update({'total':dic_asoc_RU['total']+casos_ru})
            
            dic_asoc_RS.update({e:casos_rs})
            dic_asoc_RS.update({'total':dic_asoc_RS['total']+casos_rs})
            
            estado.update({e:casos_ru + casos_rs})
            
        tipo.append(dic_asoc_RU)
        tipo.append(dic_asoc_RS)
        
        total = q_ru.count()+q_rs.count()
        
        extras.append({
            'nombre':'Sin TU asoc.',
            'cantidad':total - q_ru.filter(tiposUsuario__vigencia=True).distinct().count() - q_rs.filter(tiposUsuario__vigencia=True).distinct().count()
        })
        
        cp.update({'atributos':[tipo]})
        cp.update({'estado':estado})
        cp.update({'extras':extras})
        cp.update({'total':total})
        
        # estadisticas de modulos
        q = Modulo.objects.vigentes(proyecto)
        md = {}
        prioridad = []
        extras = []
        
        tabla = [
            ('prioridad', 'prioridad', PRIORIDAD_CHOICES, prioridad),
        ]
        
        for atributo, s, choices, arreglo in tabla:
            dic = {'atributo':atributo,'atributos':len(choices)}
            for key, nombre in choices:
                dic.update({'nombre':nombre})
                qq = q.filter(prioridad=key)
                total = qq.count()
                dic.update({'total':total})
                arreglo.append(dic)
                dic = {}
        
        total = q.count()
        extras.append({
            'nombre':'Sin RS asoc.',
            'cantidad':total - q.filter(requisitosSoftware__vigencia=True).distinct().count()
        })
        costo = 0
        for dic in q.values('costo'):
            costo = costo + dic['costo']
        extras.append({
            'nombre':'Costo total',
            'cantidad':costo
        })
        
        md.update({'atributos':[prioridad]})
        md.update({'extras':extras})
        md.update({'total':total})
    else:
        raise Http404
    context = {
        'navbar':navbar,
        'HT_CHOICES':HT_CHOICES,
        'hito':hito,
        'RU':ru,
        'RS':rs,
        'MD':md,
        'CP':cp,
    }
    return render(request, 'reqApp/herramientas/estadisticas/estadisticas.html', context)

##############################  MATRICES DE TRAZADO
MATRIZ_CHOICES = [
    ("rurs", "RU/RS"),
    ("mdrs", "MD/RS"),
    ("rucp", "RU/CP"),
    ("rscp", "RS/CP"),
]

def matrixSplit(rows, maxRows, maxCols):
    # para subdividir la matriz en cuadrantes para la impresion en .pdf
    # TODO
    return [rows]

def matrixMatch(elemento1, elemento2, proyecto):
    return len(RequisitoSoftware.objects.vigentes(proyecto).filter(id=requisitoSoftware.id).filter(requisitosUsuario=self))>0

def matriz(tipo, proyecto):
    if tipo == 'rurs':
        m1s = RequisitoUsuario.objects.vigentes(proyecto)
        m2s = RequisitoSoftware.objects.vigentes(proyecto)
        
        m2idsmatchs = []
        for fila in range(0,len(m1s)):
            m2idsmatchs.append([])
            for rs in m2s.filter(requisitosUsuario=m1s[fila]):
                m2idsmatchs[fila].append(rs.id)
                
        colNoIntersec = []
        for rs in m2s:
            colNoIntersec.append(len(m1s.filter(requisitosoftware=rs))==0)
    elif tipo == 'mdrs':
        m1s = Modulo.objects.vigentes(proyecto)
        m2s = RequisitoSoftware.objects.vigentes(proyecto)
        
        m2idsmatchs = []
        for fila in range(0,len(m1s)):
            m2idsmatchs.append([])
            for rs in m2s.filter(modulo=m1s[fila]):
                m2idsmatchs[fila].append(rs.id)
                
        colNoIntersec = []
        for rs in m2s:
            colNoIntersec.append(len(m1s.filter(requisitosSoftware=rs))==0)
    elif tipo == 'rucp':
        m1s = RequisitoUsuario.objects.vigentes(proyecto)
        m2s = CasoPrueba.objects.vigentes(proyecto)
        
        m2idsmatchs = []
        for fila in range(0,len(m1s)):
            m2idsmatchs.append([])
            for cp in m2s.filter(requisito=m1s[fila]):
                m2idsmatchs[fila].append(cp.id)
                
        colNoIntersec = []
        for cp in m2s:
            colNoIntersec.append(len(m1s.filter(casoprueba=cp))==0)
    elif tipo == 'rscp':
        m1s = RequisitoSoftware.objects.vigentes(proyecto)
        m2s = CasoPrueba.objects.vigentes(proyecto)
        
        m2idsmatchs = []
        for fila in range(0,len(m1s)):
            m2idsmatchs.append([])
            for cp in m2s.filter(requisito=m1s[fila]):
                m2idsmatchs[fila].append(cp.id)
                
        colNoIntersec = []
        for cp in m2s:
            colNoIntersec.append(len(m1s.filter(casoprueba=cp))==0)
        
    filas = []
    for fila in range(0,len(m1s)):
        filas.append([])
        
        for col in range(0,len(m2s)):
            match = m2s[col].id in m2idsmatchs[fila]
            filas[fila].append({
                'elFila':m1s[fila],
                'elCol':m2s[col],
                'fila':fila,
                'col':col,
                'match':match,
                'no_intersec':((len(m2idsmatchs[fila])==0)or(colNoIntersec[col])),
                })
    return filas

def matrices(request):
    usuario = get_user_or_none(request) # TODO is None?
    proyecto = proyectoDeUsuario(usuario)
    navbar = {'1':'herramientas', '2':'matrices'}
    
    tipo =  request.GET.get('tipo', 'rurs')
    filas = matriz(tipo, proyecto)
    context = {
        'navbar':navbar,
        'filas':filas,
        'MATRIZ_CHOICES':MATRIZ_CHOICES,
        'tipo':tipo,
    }
    return render(request, 'reqApp/herramientas/matrices/matrices.html', context)

##############################  CONSISTENCIA
def consistencia(request):
    navbar = {'1':'herramientas', '2':'consistencia'}
    return herrView(request, navbar)

##############################  BITACORA
def bitacora(request):
    TIPOS_CHOICES = [
        ("ht", "Hitos"),
        ("tu", "Tipos de Usuario"),
        ("ru", "Requisitos de Usuario"),
        ("rs", "Requisitos de Software"),
        ("md", "Módulos"),
        ("cp", "Casos de Prueba"),
    ]
    IDENTIFICADOR_CHOICES = [
        (0, "Todos"),
    ]
    models = {
        "ht": Hito,
        "tu": TipoUsuario,
        "ru": RequisitoUsuario,
        "rs": RequisitoSoftware,
        "md": Modulo,
        "cp": CasoPrueba,
    }
    templates = {
        "ht": 'reqApp/proyecto/HT/HT.html',
        "tu": 'reqApp/proyecto/TU/TU.html',
        "ru": 'reqApp/proyecto/RU/RU.html',
        "rs": 'reqApp/proyecto/RS/RS.html',
        "md": 'reqApp/proyecto/MD/MD.html',
        "cp": 'reqApp/proyecto/CP/CP.html',    
    }
    
    usuario = get_user_or_none(request) # TODO is None?
    proyecto = proyectoDeUsuario(usuario)
    navbar = {'1':'herramientas', '2':'bitacora'}
    
    if request.method == 'GET':
        tipo =  request.GET.get('tipo', 'ru')
        
        identificador = int(request.GET.get('identificador', 0))
        
        # generar el listado de textos identificadores de elementos del tipo seleccionado
        identificadoresDict = {}
        elementos = models[tipo].objects.bitacorados(proyecto)
        for elemento in reversed(elementos):
            # el nombre correspondiente al identificador es el más reciente
            identificadoresDict.update({elemento.identificador: elemento.textoIdentificador()+" "+elemento.nombre})
        
        for key in sorted(identificadoresDict):
            IDENTIFICADOR_CHOICES.append((key, identificadoresDict[key]))
            
        if identificador > 0:
            # mostrar la evolucion del elemento con ese identificador
            elementos = models[tipo].objects.bitacorados(proyecto, identificador)
        
        # generar la lista de elementos
        listaElementos = []
        elementosDic = {}
        i = 0
        for elemento in elementos:
            borrado = False
            clave = elemento.textoIdentificador()
            if (clave not in elementosDic) and (elemento.vigencia == False):
                borrado = True
            elementosDic.update({clave:i})
            listaElementos.append({'elemento':elemento, 'actual':elemento.vigencia, 'borrado':borrado, 'nuevo':False})
            i = i + 1
        
        for key in elementosDic:
            listaElementos[elementosDic[key]]['nuevo'] = True
    else:
        raise Http404
    
    context = {
        'navbar':navbar,
        'elementos':listaElementos,
        'template':templates[tipo],
        'TIPOS_CHOICES':TIPOS_CHOICES,
        'IDENTIFICADOR_CHOICES':IDENTIFICADOR_CHOICES,
        'tipo':tipo,
        'identificador':identificador,
    }
    return render(request, 'reqApp/herramientas/bitacora/bitacora.html', context)
    
############################### MCE ##########################
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

#@csrf_exempt
@require_POST
def imgUpload(request):
    usuario = get_user_or_none(request) # TODO is None?
    proyecto = proyectoDeUsuario(usuario)
    
    upload_path = getattr(settings, 'IMAGES_UPLOAD', 'uploads/') + str(proyecto.id) +'/'
    form = MceImageForm(request.POST, request.FILES)
    if form.is_valid():
        file_ = form.cleaned_data['file']
        path = os.path.join(upload_path, file_.name)
        real_path = default_storage.save(path, file_)
        return HttpResponse(
            os.path.join(settings.MEDIA_URL, real_path)
        )
    return HttpResponse('')
    
############################### PDF ##########################
from django.template.loader import get_template
from django.template import Context
import xhtml2pdf.pisa as pisa
import cStringIO as StringIO

def pdfIndex(request):
    #print request.build_absolute_uri("/") # --> http://127.0.0.1:8000/download/
    return HttpResponse("""
        <html><body>
            <h1>Example 1</h1>
            Please enter some HTML code:
            <form action="/download/" method="post" enctype="multipart/form-data">
            <textarea name="data">Hello <strong>World</strong></textarea>
            <br />
            <input type="submit" value="Convert HTML to PDF" />
            </form>
            <hr>
            <h1>Example 2</h1>
            <p><a href="/ezpdf_sample">Example with template</a></p>
        </body></html>
        """)
@csrf_exempt
def pdfDownload(request):
    #print request.build_absolute_uri() # --> http://127.0.0.1:8000/download/
    if request.POST:
        result = StringIO.StringIO()
        pdf = pisa.CreatePDF(
            StringIO.StringIO(request.POST["data"].encode("UTF-8")),
            result
            )

        if not pdf.err:
            return HttpResponse(
                result.getvalue(),
                mimetype='application/pdf')

    return HttpResponse('We had some errors')

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)# ...ISO-8859-1...UTF-8...latin-1... html.encode("ISO-8859-1")
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('We had some errors!')

def ezpdf_sample(request):
    blog_entries = []
    for i in range(1,10):
        blog_entries.append({
            'id': i,
            'title':'Playing with pisa 3.0.16 and dJango Template Engine',
            'body':'This is a simple example..'
            })
    return render_to_pdf('reqApp/pdf/entries.html',{
        'pagesize':'A4',
        'title':'My amazing blog',
        'blog_entries':blog_entries})
        
def pdf(request):
    usuario = get_user_or_none(request) # TODO is None?
    proyecto = proyectoDeUsuario(usuario)
    context = {
        'hoja':'letter',# https://github.com/chrisglass/xhtml2pdf/blob/master/doc/usage.rst#supported-page-properties-and-values
        'titulo':'',
        'host':request.build_absolute_uri("/")[:-1],# http://localhost:8000
        'proyecto':proyecto,
        'hoy':timezone.now(),
    }
    if request.method == 'GET':
        tipo =  request.GET.get('tipo', '')
        if tipo == 'docReq':
            template = 'reqApp/pdf/documentos/requisitos.html'
            secciones = [
                {'titulo':'1. Introducción','contenido':Documento.objects.vigente(proyecto,'introduccion')},
                {'titulo':'1.1. Propósito','contenido':Documento.objects.vigente(proyecto,'proposito')},
                {'titulo':'1.2. Alcance','contenido':Documento.objects.vigente(proyecto,'alcance')},
                {'titulo':'1.3. Contexto','contenido':Documento.objects.vigente(proyecto,'contexto')},
                {'titulo':'1.4. Definiciones','contenido':Documento.objects.vigente(proyecto,'definiciones')},
                {'titulo':'1.5. Referencias','contenido':Documento.objects.vigente(proyecto,'referencias')},
                {'titulo':'2. Descripción General','contenido':Documento.objects.vigente(proyecto,'descripcion_general')},
                {'titulo':'2.1. Usuarios','contenido':Documento.objects.vigente(proyecto,'usuarios')},
                {'titulo':'2.2. Producto','contenido':Documento.objects.vigente(proyecto,'producto')},
                {'titulo':'2.3. Ambiente','contenido':Documento.objects.vigente(proyecto,'ambiente')},
                {'titulo':'2.4. Proyectos Relacionados','contenido':Documento.objects.vigente(proyecto,'proyectos_relacionados')},
            ]
            context.update({
                'titulo':'Documento de Especificación de Requisitos de Usuario/Software',
                'secciones':secciones,
            })
        elif tipo == 'RU':
            template = 'reqApp/pdf/proyecto/RU/RU.html'
            context.update({
                'titulo':'Requisitos de Usuario',
                'RUs':RequisitoUsuario.objects.vigentes(proyecto,'tipo'),
            })
        elif tipo == 'RS':
            template = 'reqApp/pdf/proyecto/RS/RS.html'
            context.update({
                'titulo':'Requisitos de Software',
                'RSs':RequisitoSoftware.objects.vigentes(proyecto,'tipo'),
            })
        elif tipo == 'TU':
            template = 'reqApp/pdf/proyecto/TU/TU.html'
            context.update({
                'titulo':'Tipos de Usuario',
                'TUs':TipoUsuario.objects.vigentes(proyecto),
            })
        elif tipo == 'MD':
            template = 'reqApp/pdf/proyecto/MD/MD.html'
            context.update({
                'titulo':'Módulos',
                'MDs':Modulo.objects.vigentes(proyecto),
            })
        elif tipo == 'CP':
            template = 'reqApp/pdf/proyecto/CP/CP.html'
            context.update({
                'titulo':'Casos de Prueba',
                'CPs':CasoPrueba.objects.vigentes(proyecto),
            })
        elif tipo == 'HT':
            template = 'reqApp/pdf/proyecto/HT/HT.html'
            context.update({
                'titulo':'Hitos',
                'HTs':Hito.objects.vigentes(proyecto),
            })
        elif tipo == 'MT':
            template = 'reqApp/pdf/herramientas/matrices/MT.html'
            matrices = []
            for tipo,nombre in MATRIZ_CHOICES:
                matrices.append({
                    'nombre':nombre,
                    'filas':matriz(tipo,proyecto)
                })
            
            #
            mTs = []
            
            myFilas = []
            for f in range(0, 80):
                fila = []
                for c in range(0, 50):
                    sol = 'CL%04d' % c
                    fila.append({
                        "fila":'FL%04d' % f,
                        "col":sol,
                        "col0":sol[0],
                        "col1":sol[1],
                        "col2":sol[2],
                        "col3":sol[3],
                        "col4":sol[4],
                        "col5":sol[5],
                    })
                myFilas.append(fila)
                
            mTs.append({
                'nombre':'FUAA/WEE',
                'subMTs':matrixSplit(myFilas, 10, 10),
            })
            #
            context.update({
                'titulo':'Matrices de Trazado',
                'MTs':mTs,#mTs, matrices, TODO
            })
        else:
            raise Http404
    else:
        raise Http404
    return render_to_pdf(template,context)
