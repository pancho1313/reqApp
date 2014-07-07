# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from reqApp.forms import *
from reqApp.util import *
from django.contrib.auth.models import User
#from django.utils import simplejson
import json

from django.http import HttpResponse
from django.http import Http404

from django.db.models import Sum

################ after login ################
def selectProject(request):
    usuario = get_user_or_none(request) # TODO is None?
    if usuario is not None:
        if request.method == 'GET':
            if usuario.userprofile.proyectos.count() == 1:
                request.session['project'] = 0
            else:
                projects = []
                for i,p in enumerate(usuario.userprofile.proyectos.all().order_by('-id')):
                    projects.append((i,p))
                context = {
                    'projects':projects,
                }
                return render(request, 'reqApp/selectProject.html', context)
        else:
            if 'index' in request.POST:
                index = int(request.POST['index'])
                request.session['project'] = index
                print getProject(request)#checking
        return HttpResponseRedirect(reverse('reqApp:RU'))
    raise Http404

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

def elementView(request, mensajes, modelFormClass, elementTemplate, formTemplate, modelClass, navbar, pdfLink=None, helpLink=None):
    usuario = get_user_or_none(request) # TODO is None?
    proyecto = getProject(request)
    if request.method == 'POST':
        if 'identificador' in request.POST:# editar o borrar
            identificador = request.POST['identificador']
            instance = modelClass.objects.vigente(proyecto, identificador)
            if 'borrar' in request.POST:# borrar elemento
                instance.bitacorarElementoBorrado(usuario)
                mensajes.append(instance.textoIdentificador()+u' borrado y registrado en la bitácora')
            else:# editar elemento
                form = modelFormClass(instance=instance, data=request.POST)
                if form.is_valid():
                    if request.POST.has_key("solo_validar"):
                        return ajax_form_valid(form, True)
                    form.asignarProyecto(proyecto)
                    form.actualizarElementoDeBitacora(usuario, identificador)
                    mensajes.append(instance.textoIdentificador()+u' modificado y registrado en la bitácora')
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
                instance = form.crearElementoDeBitacora(usuario)
                mensajes.append(instance.textoIdentificador()+u' creado')
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
        'atributos_ordenables': orderingList(modelClass),
        'orden_actual': ordenActual,
        'navbar':navbar,
        'pdfLink':pdfLink,
        'helpLink':helpLink,
    }
    return render(request, 'reqApp/proyecto/lista_expandible.html', context)

def viewTU(request):
    mensajes = []
    navbar = {'1':'proyecto', '2':'TU'}
    return elementView(request, mensajes, TUForm, 'reqApp/proyecto/TU/TU.html', 'reqApp/proyecto/TU/TU_form.html', TipoUsuario, navbar, 'TU', 'TU')

def viewRU(request):
    mensajes = []
    navbar = {'1':'proyecto', '2':'RU'}
    return elementView(request, mensajes, RUForm, 'reqApp/proyecto/RU/RU.html', 'reqApp/proyecto/RU/RU_form.html', RequisitoUsuario, navbar, 'RU', 'RU')

def viewRS(request):
    mensajes = []
    navbar = {'1':'proyecto', '2':'RS'}
    return elementView(request, mensajes, RSForm, 'reqApp/proyecto/RS/RS.html', 'reqApp/proyecto/RS/RS_form.html', RequisitoSoftware, navbar, 'RS', 'RS')

def viewMD(request):
    mensajes = []
    navbar = {'1':'proyecto', '2':'MD'}
    return elementView(request, mensajes, MDForm, 'reqApp/proyecto/MD/MD.html', 'reqApp/proyecto/MD/MD_form.html', Modulo, navbar, 'MD', 'MD')

def viewCP(request):
    mensajes = []
    navbar = {'1':'proyecto', '2':'CP'}
    return elementView(request, mensajes, CPForm, 'reqApp/proyecto/CP/CP.html', 'reqApp/proyecto/CP/CP_form.html', CasoPrueba, navbar, 'CP', 'CP')
    
def viewHT(request):
    mensajes = []
    navbar = {'1':'proyecto', '2':'HT'}
    return elementView(request, mensajes, HTForm, 'reqApp/proyecto/HT/HT.html', 'reqApp/proyecto/HT/HT_form.html', Hito, navbar, 'HT', 'HT')
    
################################# Documentos #############################
def docView(request, navbar, activos, pdfLink):
    usuario = get_user_or_none(request) # TODO is None?
    proyecto = getProject(request)

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
        'pdfLink':pdfLink,
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
    return docView(request, navbar, parrafos, 'docReq')
    
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
    return docView(request, navbar, parrafos, 'docDis')
    
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
    return docView(request, navbar, parrafos, 'docCP')

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
    return docView(request, navbar, parrafos, 'docHis')

############################### Herramientas ##########################

##############################  TAREAS
def tareas(request):
    navbar = {'1':'herramientas', '2':'tareas'}
    context = {
        'navbar':navbar,
    }
    return render(request, 'reqApp/herramientas/tareas/tareas.html', context)

##############################  ESTADISTICAS
def estadisticasRU_RS_CP_MD(proyecto, ht=None):
    # estadisticas de requisitos de usuario
    q = RequisitoUsuario.objects.vigentes(proyecto).filter(hito__vigencia=True)
    if ht is not None:
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
    if ht is not None:
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
    
    if ht is not None:
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
    
    return {
        'RU':ru,
        'RS':rs,
        'CP':cp,
        'MD':md,
    }
    
def estadisticas(request):
    HT_CHOICES = [
        (0, "Todos"),
    ]

    usuario = get_user_or_none(request) # TODO is None?
    proyecto = getProject(request)
    navbar = {'1':'herramientas', '2':'estadisticas'}
    
    if request.method == 'GET':
        hito = int(request.GET.get('hito', 0))
        nombreHito = ''
        hitos = Hito.objects.vigentes(proyecto)
        for ht in hitos:
            HT_CHOICES.append((ht.identificador,ht.nombre))
            if ht.identificador == hito:
                nombreHito = ht.nombre
        if hito > 0:
            ht = hitos.get(identificador=hito)
        else:# todos los Hitos
            ht = None
            
        estDic = estadisticasRU_RS_CP_MD(proyecto, ht)
    else:
        raise Http404
    context = {
        'navbar':navbar,
        'HT_CHOICES':HT_CHOICES,
        'hito':hito,
        'nombreHito':nombreHito,
        'RU':estDic['RU'],
        'RS':estDic['RS'],
        'MD':estDic['MD'],
        'CP':estDic['CP'],
    }
    return render(request, 'reqApp/herramientas/estadisticas/estadisticas.html', context)

##############################  MATRICES DE TRAZADO
MATRIZ_CHOICES = [
    ("rurs", "Matriz RU/RS"),
    ("mdrs", "Matriz MD/RS"),
    ("rucp", "Matriz RU/CP"),
    ("rscp", "Matriz RS/CP"),
]

def matrixSplit(rows, maxRows, maxCols):
    # para subdividir la matriz en cuadrantes para la impresion en .pdf
    """
                 |abcde|             |abc|  |de|
    matrixSplit( |fghij| , 2, 3) --> |fgh|  |ij|  |klm|  |no|
                 |klmno|
    """
    if len(rows)>0:
        if len(rows[0])>0:
            hiperRows = []
            hrows = int(len(rows)/maxRows)
            if len(rows)%maxRows > 0:
                hrows = hrows + 1
            
            hcols = int(len(rows[0])/maxCols)
            if len(rows[0])%maxCols > 0:
                hcols = hcols + 1
                
            for x in range(0,hcols*hrows):
                hiperRows.append([])
                
            for r,row in enumerate(rows):
                fillingRow = []
                for c,el in enumerate(row):
                    # posicionar el elemento en la nueva fila
                    fillingRow.append(el)
                    
                    # si completamos una fila o era el ultimo elemento de la fila
                    if len(fillingRow)==maxCols or (c+1)==len(row):
                        hiperRows[int((c)/maxCols)+(hcols*int((r)/maxRows))].append(fillingRow)
                        fillingRow = []
            
            return hiperRows
            
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
        m2s = CasoPrueba.objects.vigentes(proyecto).filter(requisito__in=RequisitoUsuario.objects.bitacorados(proyecto))
        
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
        m2s = CasoPrueba.objects.vigentes(proyecto).filter(requisito__in=RequisitoSoftware.objects.bitacorados(proyecto))
        
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
            fila_no_intersec = (len(m2idsmatchs[fila])==0)
            filas[fila].append({
                'elFila':m1s[fila],
                'elCol':m2s[col],
                'fila':fila,
                'col':col,
                'match':match,
                'nunca_intersec':(fila_no_intersec and colNoIntersec[col]),
                'fila_no_intersec':fila_no_intersec,
                'col_no_intersec':colNoIntersec[col],
                })
    return filas

def matrices(request):
    usuario = get_user_or_none(request) # TODO is None?
    proyecto = getProject(request)
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
def arbolDeRelaciones(modelQSet, subModelQSet, prop, identificador):
    resp = []
    if identificador > 0:
        elements = modelQSet.filter(identificador=identificador)
    else:
        elements = modelQSet
    for e in elements:
        subElementos = subModelQSet.filter(**myFilter(prop,e))
        resp.append({'elemento':e,'subElementos':subElementos})
    return resp

def consistencia(request):
    CONSISTENCIA_CHOICES = [
        ("rurs", "Consistencia RU/RS"),
        ("rucp", "Consistencia RU/CP"),
        ("rsru", "Consistencia RS/RU"),
        ("rscp", "Consistencia RS/CP"),
        ("rsmd", "Consistencia RS/MD"),
        ("mdrs", "Consistencia MD/RS"),
        ("cpru", "Consistencia CP/RU"),
        ("cprs", "Consistencia CP/RS"),
    ]
    IDENTIFICADOR_CHOICES = [
        (0, "Todos"),
    ]
    templates = {
        "rurs":{'elemento':'reqApp/proyecto/RU/RU.html','subElemento':'reqApp/proyecto/RS/RS.html'},
        "rucp":{'elemento':'reqApp/proyecto/RU/RU.html','subElemento':'reqApp/proyecto/CP/CP.html'},
        "rsru":{'elemento':'reqApp/proyecto/RS/RS.html','subElemento':'reqApp/proyecto/RU/RU.html'},
        "rscp":{'elemento':'reqApp/proyecto/RS/RS.html','subElemento':'reqApp/proyecto/CP/CP.html'},
        "rsmd":{'elemento':'reqApp/proyecto/RS/RS.html','subElemento':'reqApp/proyecto/MD/MD.html'},
        "mdrs":{'elemento':'reqApp/proyecto/MD/MD.html','subElemento':'reqApp/proyecto/RS/RS.html'},
        "cpru":{'elemento':'reqApp/proyecto/CP/CP.html','subElemento':'reqApp/proyecto/RU/RU.html'},
        "cprs":{'elemento':'reqApp/proyecto/CP/CP.html','subElemento':'reqApp/proyecto/RS/RS.html'},
    }
    
    usuario = get_user_or_none(request) # TODO is None?
    proyecto = getProject(request)
    navbar = {'1':'herramientas', '2':'consistencia'}
    
    if request.method == 'GET':
        consistencia =  request.GET.get('consistencia', 'rurs')
        identificador = int(request.GET.get('identificador', 0))
        
        ordenActual = 'identificador'
        if 'orden' in request.GET:
            ordenActual = request.GET['orden']
        
        elementos = []
        if consistencia == 'rurs':
            model = RequisitoUsuario
            modeloQ = RequisitoUsuario.objects.vigentes(proyecto)
            subModeloQ = RequisitoSoftware.objects.vigentes(proyecto)
            prop = 'requisitosUsuario'
        elif consistencia == 'rucp':
            model = RequisitoUsuario
            modeloQ = RequisitoUsuario.objects.vigentes(proyecto)
            subModeloQ = CasoPrueba.objects.vigentes(proyecto)
            prop = 'requisito'
        elif consistencia == 'rsru':
            model = RequisitoSoftware
            modeloQ = RequisitoSoftware.objects.vigentes(proyecto)
            subModeloQ = RequisitoUsuario.objects.vigentes(proyecto)
            prop = 'requisitosoftware'
        elif consistencia == 'rscp':
            model = RequisitoSoftware
            modeloQ = RequisitoSoftware.objects.vigentes(proyecto)
            subModeloQ = CasoPrueba.objects.vigentes(proyecto)
            prop = 'requisito'
        elif consistencia == 'rsmd':
            model = RequisitoSoftware
            modeloQ = RequisitoSoftware.objects.vigentes(proyecto)
            subModeloQ = Modulo.objects.vigentes(proyecto)
            prop = 'requisitosSoftware'
        elif consistencia == 'mdrs':
            model = Modulo
            modeloQ = Modulo.objects.vigentes(proyecto)
            subModeloQ = RequisitoSoftware.objects.vigentes(proyecto)
            prop = 'modulo'
        elif consistencia == 'cpru':
            model = CasoPrueba
            modeloQ = CasoPrueba.objects.vigentes(proyecto).filter(requisito__in=RequisitoUsuario.objects.bitacorados(proyecto))
            subModeloQ = RequisitoUsuario.objects.vigentes(proyecto)
            prop = 'casoprueba'
        elif consistencia == 'cprs':
            model = CasoPrueba
            modeloQ = CasoPrueba.objects.vigentes(proyecto).filter(requisito__in=RequisitoSoftware.objects.bitacorados(proyecto))
            subModeloQ = RequisitoSoftware.objects.vigentes(proyecto)
            prop = 'casoprueba'
        else:
            raise Http404
            
        # generar el listado de textos identificadores de elementos del tipo seleccionado
        identificadoresDict = {}
        elementos = modeloQ
        for elemento in elementos:
            # el nombre correspondiente al identificador es el más reciente
            identificadoresDict.update({elemento.identificador: elemento.textoIdentificador()+" "+elemento.nombre})
        for key in sorted(identificadoresDict):
            IDENTIFICADOR_CHOICES.append((key, identificadoresDict[key]))
            
        elementos = arbolDeRelaciones(modeloQ.order_by(ordenActual), subModeloQ, prop, identificador)
        
    else:
        raise Http404
    
    context = {
        'navbar':navbar,
        'elementos':elementos,
        'templates':templates[consistencia],
        'CONSISTENCIA_CHOICES':CONSISTENCIA_CHOICES,
        'IDENTIFICADOR_CHOICES':IDENTIFICADOR_CHOICES,
        'consistencia':consistencia,
        'identificador':identificador,
    }
    
    if identificador == 0:
        context.update({
            'atributos_ordenables': orderingList(model),
            'orden_actual': ordenActual,
            'barra_orden_elementos': 'reqApp/orden_elementos.html',
        })
    
    return render(request, 'reqApp/herramientas/consistencia/consistencia.html', context)

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
    proyecto = getProject(request)
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
    proyecto = getProject(request)
    
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

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)# ...ISO-8859-1...UTF-8...latin-1... html.encode("ISO-8859-1")
    if not pdf.err:
        resp = HttpResponse(result.getvalue(), mimetype='application/pdf')
        resp['Content-Disposition'] = u'filename='+context_dict['nombreArchivo']+u'.pdf'
        return resp
    return HttpResponse('We had some errors!')
        
def pdf(request):
    usuario = get_user_or_none(request) # TODO is None?
    proyecto = getProject(request)
    context = {
        'hoja':'letter',# https://github.com/chrisglass/xhtml2pdf/blob/master/doc/usage.rst#supported-page-properties-and-values
        'titulo':'',
        'nombreArchivo':'',
        'host':request.build_absolute_uri("/")[:-1],# http://localhost:8000
        'proyecto':proyecto,
        'hoy':timezone.now(),
    }
    
    # ancho y largo maximo en caracteres de la tabla generada antes de ser particionada para ajustarse en la pag .pdf
    # WARNING: estos valores deberían ser reajustados ante un cambio de "pagesize" (letter, A4, ...)
    ANCHO_MTs = 50
    LARGO_MTs = 50
    
    if request.method == 'GET':
        tipo =  request.GET.get('tipo', '')
        if tipo == 'docReq':
            template = 'reqApp/pdf/documentos/requisitos.html'
            secciones = [
                {'titulo':'<h1>1. Introducción</h1>',            'contenido':Documento.objects.vigente(proyecto,'introduccion')},
                {'titulo':'<h2>1.1. Propósito</h2>',             'contenido':Documento.objects.vigente(proyecto,'proposito')},
                {'titulo':'<h2>1.2. Alcance</h2>',               'contenido':Documento.objects.vigente(proyecto,'alcance')},
                {'titulo':'<h2>1.3. Contexto</h2>',              'contenido':Documento.objects.vigente(proyecto,'contexto')},
                {'titulo':'<h2>1.4. Definiciones</h2>',          'contenido':Documento.objects.vigente(proyecto,'definiciones')},
                {'titulo':'<h2>1.5. Referencias</h2>',           'contenido':Documento.objects.vigente(proyecto,'referencias')},
                {'titulo':'<h1>2. Descripción General</h1>',     'contenido':Documento.objects.vigente(proyecto,'descripcion_general')},
                {'titulo':'<h2>2.1. Usuarios</h2>',              'contenido':Documento.objects.vigente(proyecto,'usuarios')},
                {'titulo':'<h2>2.2. Producto</h2>',              'contenido':Documento.objects.vigente(proyecto,'producto')},
                {'titulo':'<h2>2.3. Ambiente</h2>',              'contenido':Documento.objects.vigente(proyecto,'ambiente')},
                {'titulo':'<h2>2.4. Proyectos Relacionados</h2>','contenido':Documento.objects.vigente(proyecto,'proyectos_relacionados')},
            ]
            
            
            context.update({
                'titulo':'Documento de Especificación de Requisitos de Usuario/Software',
                'nombreArchivo':'Documento_de_Requisitos',
                'secciones':secciones,
                'RUs':RequisitoUsuario.objects.vigentes(proyecto,'tipo'),
                'RSs':RequisitoSoftware.objects.vigentes(proyecto,'tipo'),
                'MTs':[{
                    'nombre':'RU/RS',
                    'subMTs':matrixSplit(matriz('rurs',proyecto), LARGO_MTs, ANCHO_MTs)
                    }],
            })
        elif tipo == 'docDis':
            template = 'reqApp/pdf/documentos/diseno.html'
            secciones = [
                {'titulo':'<h1>1. Introducción</h1>',            'contenido':Documento.objects.vigente(proyecto,'introduccion')},
                {'titulo':'<h2>1.1. Propósito</h2>',             'contenido':Documento.objects.vigente(proyecto,'proposito')},
                {'titulo':'<h2>1.2. Alcance</h2>',               'contenido':Documento.objects.vigente(proyecto,'alcance')},
                {'titulo':'<h2>1.3. Contexto</h2>',              'contenido':Documento.objects.vigente(proyecto,'contexto')},
                {'titulo':'<h2>1.4. Definiciones</h2>',          'contenido':Documento.objects.vigente(proyecto,'definiciones')},
                {'titulo':'<h2>1.5. Referencias</h2>',           'contenido':Documento.objects.vigente(proyecto,'referencias')},
                {'titulo':'<h1>2. Descripción General</h1>',     'contenido':Documento.objects.vigente(proyecto,'descripcion_general')},
                
                {'titulo':'<h1>3. Diseño</h1>',                  'contenido':Documento.objects.vigente(proyecto,'diseno')},
                {'titulo':'<h2>3.1. Arquitectura Física</h2>',   'contenido':Documento.objects.vigente(proyecto,'arquitectura_fisica')},
                {'titulo':'<h2>3.2. Arquitectura Lógica</h2>',   'contenido':Documento.objects.vigente(proyecto,'arquitectura_logica')},
                {'titulo':'<h2>3.3. Modelo de Datos</h2>',       'contenido':Documento.objects.vigente(proyecto,'modelo')},
                
                {'titulo':'<h2>3.4. Detalle Módulos</h2>',       'contenido':Documento.objects.vigente(proyecto,'detalle_modulos')},
                {'titulo':'<h2>3.5. Navegación</h2>',            'contenido':Documento.objects.vigente(proyecto,'navegacion')},
                {'titulo':'<h2>3.6. Interfaz</h2>',              'contenido':Documento.objects.vigente(proyecto,'interfaz')},
            ]
            
            context.update({
                'titulo':'Documento de Diseño',
                'nombreArchivo':'Documento_de_Diseno',
                'secciones':secciones,
                'MDs':Modulo.objects.vigentes(proyecto),
                'MTs':[{
                    'nombre':'MD/RS',
                    'subMTs':matrixSplit(matriz('mdrs',proyecto), LARGO_MTs, ANCHO_MTs)
                    }],
            })
        elif tipo == 'docCP':
            template = 'reqApp/pdf/documentos/cp.html'
            secciones = [
                {'titulo':'<h1>1. Introducción</h1>',            'contenido':Documento.objects.vigente(proyecto,'introduccion')},
                {'titulo':'<h2>1.1. Propósito</h2>',             'contenido':Documento.objects.vigente(proyecto,'proposito')},
                {'titulo':'<h2>1.2. Alcance</h2>',               'contenido':Documento.objects.vigente(proyecto,'alcance')},
                {'titulo':'<h2>1.3. Contexto</h2>',              'contenido':Documento.objects.vigente(proyecto,'contexto')},
                {'titulo':'<h2>1.4. Definiciones</h2>',          'contenido':Documento.objects.vigente(proyecto,'definiciones')},
                {'titulo':'<h2>1.5. Referencias</h2>',           'contenido':Documento.objects.vigente(proyecto,'referencias')},
                {'titulo':'<h1>2. Descripción General</h1>',     'contenido':Documento.objects.vigente(proyecto,'descripcion_general')},
                {'titulo':'<h2>2.1. Usuarios</h2>',              'contenido':Documento.objects.vigente(proyecto,'usuarios')},
                {'titulo':'<h2>2.2. Producto</h2>',              'contenido':Documento.objects.vigente(proyecto,'producto')},
                {'titulo':'<h2>2.3. Ambiente</h2>',              'contenido':Documento.objects.vigente(proyecto,'ambiente')},
                {'titulo':'<h2>2.4. Proyectos Relacionados</h2>','contenido':Documento.objects.vigente(proyecto,'proyectos_relacionados')},
            ]
            
            
            context.update({
                'titulo':'Documento de Casos de Prueba',
                'nombreArchivo':'Documento_Casos_de_Prueba',
                'secciones':secciones,
                'RUs':RequisitoUsuario.objects.vigentes(proyecto,'tipo'),
                'RSs':RequisitoSoftware.objects.vigentes(proyecto,'tipo'),
                'CPs':CasoPrueba.objects.vigentes(proyecto),
                'MTs':[{
                    'nombre':'RU/RS',
                    'subMTs':matrixSplit(matriz('rurs',proyecto), LARGO_MTs, ANCHO_MTs)
                    },{
                    'nombre':'RU/CP',
                    'subMTs':matrixSplit(matriz('rucp',proyecto), LARGO_MTs, ANCHO_MTs)
                    },{
                    'nombre':'RS/CP',
                    'subMTs':matrixSplit(matriz('rscp',proyecto), LARGO_MTs, ANCHO_MTs)
                    }],
            })
        elif tipo == 'docHis':
            template = 'reqApp/pdf/documentos/historico.html'
            secciones = [
                {'titulo':'<h1>1. Introducción</h1>',            'contenido':Documento.objects.vigente(proyecto,'introduccion')},
                {'titulo':'<h2>1.1. Propósito</h2>',             'contenido':Documento.objects.vigente(proyecto,'proposito')},
                {'titulo':'<h2>1.2. Alcance</h2>',               'contenido':Documento.objects.vigente(proyecto,'alcance')},
                {'titulo':'<h2>1.3. Contexto</h2>',              'contenido':Documento.objects.vigente(proyecto,'contexto')},
                {'titulo':'<h2>1.4. Definiciones</h2>',          'contenido':Documento.objects.vigente(proyecto,'definiciones')},
                {'titulo':'<h2>1.5. Referencias</h2>',           'contenido':Documento.objects.vigente(proyecto,'referencias')},
                {'titulo':'<h1>2. Descripción General</h1>',     'contenido':Documento.objects.vigente(proyecto,'descripcion_general')},
                {'titulo':'<h2>2.1. Usuarios</h2>',              'contenido':Documento.objects.vigente(proyecto,'usuarios')},
                {'titulo':'<h2>2.2. Producto</h2>',              'contenido':Documento.objects.vigente(proyecto,'producto')},
                {'titulo':'<h2>2.3. Ambiente</h2>',              'contenido':Documento.objects.vigente(proyecto,'ambiente')},
                {'titulo':'<h2>2.4. Proyectos Relacionados</h2>','contenido':Documento.objects.vigente(proyecto,'proyectos_relacionados')},
                {'titulo':'<h1>3. Diseño</h1>',                  'contenido':Documento.objects.vigente(proyecto,'diseno')},
                {'titulo':'<h2>3.1. Arquitectura Física</h2>',   'contenido':Documento.objects.vigente(proyecto,'arquitectura_fisica')},
                {'titulo':'<h2>3.2. Arquitectura Lógica</h2>',   'contenido':Documento.objects.vigente(proyecto,'arquitectura_logica')},
                {'titulo':'<h2>3.3. Modelo de Datos</h2>',       'contenido':Documento.objects.vigente(proyecto,'modelo')},
                {'titulo':'<h2>3.4. Detalle Módulos</h2>',       'contenido':Documento.objects.vigente(proyecto,'detalle_modulos')},
                {'titulo':'<h2>3.5. Navegación</h2>',            'contenido':Documento.objects.vigente(proyecto,'navegacion')},
                {'titulo':'<h2>3.6. Interfaz</h2>',              'contenido':Documento.objects.vigente(proyecto,'interfaz')},
            ]
            
            matrices = []
            for tipo,nombre in MATRIZ_CHOICES:
                matrices.append({
                    'nombre':nombre,
                    'subMTs':matrixSplit(matriz(tipo,proyecto), LARGO_MTs, ANCHO_MTs)
                })
                
            context.update({
                'titulo':'Documento Histórico',
                'nombreArchivo':'Documento_Historico',
                'secciones':secciones,
                'RUs':RequisitoUsuario.objects.vigentes(proyecto,'tipo'),
                'RSs':RequisitoSoftware.objects.vigentes(proyecto,'tipo'),
                'CPs':CasoPrueba.objects.vigentes(proyecto),
                'MDs':Modulo.objects.vigentes(proyecto),
                'MTs':matrices,
            })
        elif tipo == 'RU':
            template = 'reqApp/pdf/proyecto/RU/RU.html'
            context.update({
                'titulo':'Requisitos de Usuario',
                'nombreArchivo':'Lista_Requisitos_de_Usuario',
                'RUs':RequisitoUsuario.objects.vigentes(proyecto,'tipo'),
            })
        elif tipo == 'RS':
            template = 'reqApp/pdf/proyecto/RS/RS.html'
            context.update({
                'titulo':'Requisitos de Software',
                'nombreArchivo':'Lista_Requisitos_de_Software',
                'RSs':RequisitoSoftware.objects.vigentes(proyecto,'tipo'),
            })
        elif tipo == 'TU':
            template = 'reqApp/pdf/proyecto/TU/TU.html'
            context.update({
                'titulo':'Tipos de Usuario',
                'nombreArchivo':'Lista_Tipos_de_Usuario',
                'TUs':TipoUsuario.objects.vigentes(proyecto),
            })
        elif tipo == 'MD':
            template = 'reqApp/pdf/proyecto/MD/MD.html'
            context.update({
                'titulo':'Módulos',
                'nombreArchivo':'Lista_Modulos',
                'MDs':Modulo.objects.vigentes(proyecto),
            })
        elif tipo == 'CP':
            template = 'reqApp/pdf/proyecto/CP/CP.html'
            context.update({
                'titulo':'Casos de Prueba',
                'nombreArchivo':'Lista_Casos_de_Prueba',
                'CPs':CasoPrueba.objects.vigentes(proyecto),
            })
        elif tipo == 'HT':
            template = 'reqApp/pdf/proyecto/HT/HT.html'
            context.update({
                'titulo':'Hitos',
                'nombreArchivo':'Lista_Hitos',
                'HTs':Hito.objects.vigentes(proyecto),
            })
        elif tipo == 'MT':
            template = 'reqApp/pdf/herramientas/matrices/MT.html'
            matrices = []
            
            for tipo,nombre in MATRIZ_CHOICES:
                matrices.append({
                    'nombre':nombre,
                    'subMTs':matrixSplit(matriz(tipo,proyecto), LARGO_MTs, ANCHO_MTs)
                })
            
            ##########TODO: delete
            mTs = []
            
            myFilas = []
            for f in range(0, 80):
                fila = []
                for c in range(0, 50):
                    sol = 'CL%04d' % c
                    fila.append({
                        "fila":'FL%04d' % f,
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
            ##############
            context.update({
                'titulo':'Matrices de Trazado',
                'nombreArchivo':'Matrices_de_Trazado',
                'MTs':matrices,#mTs, matrices, TODO
            })
        elif tipo == 'ET': # estadisticas
            template = 'reqApp/pdf/herramientas/estadisticas/estadisticas.html'
            
            hitos = Hito.objects.vigentes(proyecto)
            eTs = []
            
            et = estadisticasRU_RS_CP_MD(proyecto)
            eTs.append({
                'titulo':'Estadísticas de Todo el Proyecto',
                'RU':et['RU'],
                'RS':et['RS'],
                'CP':et['CP'],
                'MD':et['MD'],
            })
            
            for ht in hitos:
                et = estadisticasRU_RS_CP_MD(proyecto, ht)
                eTs.append({
                    'titulo':u'Estadísticas '+ht.nombre,
                    'RU':et['RU'],
                    'RS':et['RS'],
                    'CP':et['CP'],
                    #'MD':et['MD'], # no lo considero porque no esta asociado a un Hito en particular
                })
            
            context.update({
                'titulo':'Estadísticas del Proyecto',
                'nombreArchivo':'Estadisticas',
                'ETs':eTs,
            })
        elif tipo == 'CT':
            template = 'reqApp/pdf/herramientas/consistencia/consistencia.html'
            
            cTs = {
                'rurs':{
                'titulo':'RU/RS',
                'nombreArchivo':'Documento_de_Consistencia_RU-RS',
                'template1':'reqApp/pdf/proyecto/RU/ru.html',
                'template2':'reqApp/pdf/proyecto/RS/rs.html',
                'elementos':arbolDeRelaciones(RequisitoUsuario.objects.vigentes(proyecto)
                                            , RequisitoSoftware.objects.vigentes(proyecto)
                                            , 'requisitosUsuario', 0)
                },
                'rucp':{
                'titulo':'RU/CP',
                'nombreArchivo':'Documento_de_Consistencia_RU-CP',
                'template1':'reqApp/pdf/proyecto/RU/ru.html',
                'template2':'reqApp/pdf/proyecto/CP/cp.html',
                'elementos':arbolDeRelaciones(RequisitoUsuario.objects.vigentes(proyecto)
                                            , CasoPrueba.objects.vigentes(proyecto)
                                            , 'requisito', 0)
                },
                'rsru':{
                'titulo':'RS/RU',
                'nombreArchivo':'Documento_de_Consistencia_RS-RU',
                'template1':'reqApp/pdf/proyecto/RS/rs.html',
                'template2':'reqApp/pdf/proyecto/RU/ru.html',
                'elementos':arbolDeRelaciones(RequisitoSoftware.objects.vigentes(proyecto)
                                            , RequisitoUsuario.objects.vigentes(proyecto)
                                            , 'requisitosoftware', 0)
                },
                'rscp':{
                'titulo':'RS/CP',
                'nombreArchivo':'Documento_de_Consistencia_RS-CP',
                'template1':'reqApp/pdf/proyecto/RS/rs.html',
                'template2':'reqApp/pdf/proyecto/CP/cp.html',
                'elementos':arbolDeRelaciones(RequisitoSoftware.objects.vigentes(proyecto)
                                            , CasoPrueba.objects.vigentes(proyecto)
                                            , 'requisito', 0)
                },
                'rsmd':{
                'titulo':'RS/MD',
                'nombreArchivo':'Documento_de_Consistencia_RS-MD',
                'template1':'reqApp/pdf/proyecto/RS/rs.html',
                'template2':'reqApp/pdf/proyecto/MD/md.html',
                'elementos':arbolDeRelaciones(RequisitoSoftware.objects.vigentes(proyecto)
                                            , Modulo.objects.vigentes(proyecto)
                                            , 'requisitosSoftware', 0)
                },
                'mdrs':{
                'titulo':'MD/RS',
                'nombreArchivo':'Documento_de_Consistencia_MD-RS',
                'template1':'reqApp/pdf/proyecto/MD/md.html',
                'template2':'reqApp/pdf/proyecto/RS/rs.html',
                'elementos':arbolDeRelaciones(Modulo.objects.vigentes(proyecto)
                                            , RequisitoSoftware.objects.vigentes(proyecto)
                                            , 'modulo', 0)
                },
                'cpru':{
                'titulo':'CP/RU',
                'nombreArchivo':'Documento_de_Consistencia_CP-RU',
                'template1':'reqApp/pdf/proyecto/CP/cp.html',
                'template2':'reqApp/pdf/proyecto/RU/ru.html',
                'elementos':arbolDeRelaciones(CasoPrueba.objects.vigentes(proyecto).filter(requisito__in=RequisitoUsuario.objects.bitacorados(proyecto))
                                            , RequisitoUsuario.objects.vigentes(proyecto)
                                            , 'casoprueba', 0)
                },
                'cprs':{
                'titulo':'CP/RS',
                'nombreArchivo':'Documento_de_Consistencia_CP-RS',
                'template1':'reqApp/pdf/proyecto/CP/cp.html',
                'template2':'reqApp/pdf/proyecto/RS/rs.html',
                'elementos':arbolDeRelaciones(CasoPrueba.objects.vigentes(proyecto).filter(requisito__in=RequisitoSoftware.objects.bitacorados(proyecto))
                                            , RequisitoSoftware.objects.vigentes(proyecto)
                                            , 'casoprueba', 0)
                },
            }
            consistencia = request.GET.get('consistencia', 'rurs')
            context.update({
                'titulo':u'Documento de Consistencia '+cTs[consistencia]['titulo'],
                'nombreArchivo':cTs[consistencia]['nombreArchivo'],
                'CTs':cTs[consistencia],
            })
        else:
            raise Http404
    else:
        raise Http404
    return render_to_pdf(template,context)
    
############################### HELP ##########################
def help(request):
    context = {}# 'helpLink'
    return render(request, 'reqApp/help.html', context)
