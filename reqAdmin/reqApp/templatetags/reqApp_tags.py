# -*- encoding: utf-8 -*-
from django import template
from reqApp.models import *
from reqApp.choices import *
from reqApp.util import *

register = template.Library()

@register.filter(name="proyecto")
def proyecto(usuario):
    return proyectoDeUsuario(usuario)

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
            
@register.filter(name="tipoReq")
def tipoReq(req):
    if req.asoc_RU():
        for key,val in TIPO_RU_CHOICES:
            if key == req.tipo:
                return val
    else:
        for key,val in TIPO_RS_CHOICES:
            if key == req.tipo:
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

@register.filter(name="porcentaje")
def porcentaje(total, parte):
    if total == 0:
        return "0%"
    return ("%3.0f" % (100*parte/total)) + "%"
    
@register.filter(name="agregarHostALosSrc")
def agregarHostALosSrc(htmlCode,host):
    # agrega el host a los src de las imagenes y otros recursos
    return htmlCode.replace('src="/','src="'+host+'/').replace("src='/","src='"+host+"/")
    
@register.filter(name="textTableHorizHeaders")
def textTableHorizHeaders(rows):
    if len(rows)>0:
        if len(rows[0])>0:
            firstRow = rows[0]
            pref = '|'
            hr = '|'
            rti = firstRow[0]['elFila'].textoIdentificador()
            for x in range(0, len(rti)):
                pref = '<span style="color:White;">o</span>'+pref#'·'+pref
                hr = '-'+hr
            hText = []
            for c in firstRow[0]['elCol'].textoIdentificador():
                hText.append('')
            for e in firstRow:
                for i,c in enumerate(e['elCol'].textoIdentificador()):
                    hText[i] = hText[i] + '<span class="' + e['elCol'].estado + '">' + c + '</span>'
            out = ''
            hrlen = 0
            for r in hText:
                hrlen = len(r)
                out = (out + pref + r + '<br/>')
            for x in range(0,len(firstRow)):
                hr = hr + '-'
            out = out + hr + '<br/>'
            
            return out
    return '---'
