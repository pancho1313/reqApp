from reqApp.models import *
from django.http import Http404
from django.core.mail import EmailMessage

def get_user_or_none(request):
    #return User.objects.get(username='alejandro')
    if request.user.is_authenticated():
        return request.user
    else:
        return None

def getProject(request):
    if 'project' not in request.session:
        raise Http404
    index = int(request.session['project'])
    projects = request.user.userprofile.proyectos
    if (index < 0) or (projects.count() < 1) or (index >= projects.count()):
        raise Http404
    else:
        return projects.all().order_by('-id')[index]
 
def myFilter(s,val):
    # para la generacion de tablas (estadisticas)
    # uso:
    #   ...filter(**myFilter('propiedad',valor))
    dic = {}
    dic[s] = val
    return dic
    
def sendEmail2User(user, subject, message):
    email = EmailMessage(subject, message, to=[user.email])
    try:
        email.send()
        return True
    except Exception, e:
        return False
    
def orderingList(model):
    # la 'posicion' corresponde al ancho(%) dentro del div (ver 'reqApp/orden_elementos.html')
    if model == TipoUsuario:
        return [
            {'orden': 'identificador', 'posicion': 15,},
            {'orden': 'nombre', 'posicion': 9,},
        ]
    elif model == RequisitoUsuario:
        return [
            {'orden': 'identificador', 'posicion': 15,},
            {'orden': 'nombre', 'posicion': 9,},
            {'orden': 'estado', 'posicion': 15,},
            {'orden': 'costo', 'posicion': 5,},
            {'orden': 'prioridad', 'posicion': 13,},
            {'orden': 'tipo', 'posicion': 18,},
            {'orden': 'hito', 'posicion': 10,},
        ]
    elif model == RequisitoSoftware:
        return [
            {'orden': 'identificador', 'posicion': 15,},
            {'orden': 'nombre', 'posicion': 9,},
            {'orden': 'estado', 'posicion': 15,},
            {'orden': 'costo', 'posicion': 5,},
            {'orden': 'prioridad', 'posicion': 13,},
            {'orden': 'tipo', 'posicion': 18,},
            {'orden': 'hito', 'posicion': 15,},
        ]
    elif model == Modulo:
        return [
            {'orden': 'identificador', 'posicion': 15,},
            {'orden': 'nombre', 'posicion': 44,},
            {'orden': 'costo', 'posicion': 8,},
            {'orden': 'prioridad', 'posicion': 10,},
        ]
    elif model == CasoPrueba:
        return [
            {'orden': 'identificador', 'posicion': 15,},
            {'orden': 'nombre', 'posicion': 9,},
            {'orden': 'estado', 'posicion': 20,},
            {'orden': 'requisito', 'posicion': 10,},
        ]
    elif model == Hito:
        return [
            {'orden': 'identificador', 'posicion': 15,},
            {'orden': 'nombre', 'posicion': 9,},
        ]
    elif model == Task:
        return [
            {'orden': 'estado', 'posicion': 45,},
            {'orden': 'fecha', 'posicion': 9,},
        ]
    return []
    
def isEditorHT(usuario):
    return usuario.has_perm('reqApp.'+Hito._meta.permissions[0][0])

def isEditorTU(usuario):
    return usuario.has_perm('reqApp.'+TipoUsuario._meta.permissions[0][0])

def isEditorRU(usuario):
    return usuario.has_perm('reqApp.'+RequisitoUsuario._meta.permissions[0][0])

def isEditorRS(usuario):
    return usuario.has_perm('reqApp.'+RequisitoSoftware._meta.permissions[0][0])

def isEditorMD(usuario):
    return usuario.has_perm('reqApp.'+Modulo._meta.permissions[0][0])

def isEditorCP(usuario):
    return usuario.has_perm('reqApp.'+CasoPrueba._meta.permissions[0][0])

def isEditorDC(usuario):
    return usuario.has_perm('reqApp.'+Documento._meta.permissions[0][0])
