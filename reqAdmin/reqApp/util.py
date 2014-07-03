from reqApp.models import *

# admin permission prefix
PERM_PRE = u"EDITOR_"

def get_user_or_none(request):
    # TODO
    """
    if request.user.is_authenticated():
        return request.user
    else:
        return None
    """
    return User.objects.get(username='alejandro')

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
