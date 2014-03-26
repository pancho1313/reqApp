from reqApp.models import *

def get_user_or_none(request):
    if request.user.is_authenticated():
        return request.user
    else:
        return None

def proyectoDeUsuario(usuario):
    # TODO: obtener el proyecto activo del usuario (en la sesion)
    return Proyecto.objects.all()[0]
