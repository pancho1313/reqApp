from django import template
from reqApp.models import *
from reqApp.choices import *

register = template.Library()

@register.filter(name="prioridad")
def prioridad(elemento):
    for key,val in PRIORIDAD_CHOICES:
        if key == elemento.prioridad:
            return val
            
@register.filter(name="tipoRU")
def tipoRU(elemento):
    for key,val in TIPO_RU_CHOICES:
        if key == elemento.tipo:
            return val
            
@register.filter(name="tipoRS")
def tipoRS(elemento):
    for key,val in TIPO_RS_CHOICES:
        if key == elemento.tipo:
            return val
            
@register.filter(name="estado")
def estado(elemento):
    for key,val in ESTADO_CHOICES:
        if key == elemento.estado:
            return val
            
@register.filter(name="enlistarVigentes")
def enlistarVigentes(queryList):
    return queryList.filter(vigencia=True).order_by('identificador')
    
@register.filter(name="enlistarRegistrados")
def enlistarRegistrados(queryList):
    return queryList.order_by('identificador')
    
@register.filter(name="largoLista")
def largoLista(lista):
    return len(lista)
