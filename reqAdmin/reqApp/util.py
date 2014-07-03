from reqApp.models import *
from django.http import Http404

def get_user_or_none(request):
    #return User.objects.get(username='alejandro')
    if request.user.is_authenticated():
        return request.user
    else:
        return None

def getProject(request):
    index = int(request.session['project'])
    projects = request.user.userprofile.proyectos
    if (index < 0) or (projects.count() < 1) or (index >= projects.count()):
        raise Http404
    else:
        return projects.all().order_by('-id')[index]
        

def proyectoDeUsuario(usuario):
    # TODO: obtener el proyecto activo del usuario (en la sesion)
    return Proyecto.objects.all()[1]
    
def myFilter(s,val):
    # para la generacion de tablas (estadisticas)
    # uso:
    #   ...filter(**myFilter('propiedad',valor))
    dic = {}
    dic[s] = val
    return dic
    
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
