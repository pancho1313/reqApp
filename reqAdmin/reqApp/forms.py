# -*- encoding: utf-8 -*-
from django import forms
from reqApp.models import *
from django.utils import timezone

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre', 'descripcion']

class BitacoraForm(forms.ModelForm):
    camposVigentesDelProyecto = []
    def asignarProyecto(self, proyecto):
        self.proyecto = proyecto
        
        # estos campos solo consideran elementos vigentes del proyecto ordenados por identificador
        for campo in self.camposVigentesDelProyecto:
            self.fields[campo].queryset = self.fields[campo].queryset.filter(vigencia=True).filter(proyecto=self.proyecto).order_by('identificador')
            
        return self
        
    def bitacorarElemento(self, usuario, identificador=None):
        # https://docs.djangoproject.com/en/1.6/topics/forms/modelforms/#the-save-method
        elemento = self.save(commit=False)
        
        if identificador == None: # crear un elemento nuevo
            # crear nuevo registro en la base de datos
            elemento.bitacorarNuevoElemento(self.proyecto, usuario)
            
        else: # editar elemento
            # registrar una copia no vigente en la bitacora
            elemento.bitacorarCopiaDeElemento(self.proyecto, identificador)
            
            # registrar nuevo estado en la base de datos
            elemento.bitacorarElemento(usuario)
        
        # actualizar relaciones "many2many"
        self.save_m2m()
    
    def crearElementoDeBitacora(self, usuario):
        self.bitacorarElemento(usuario)
    
    def actualizarElementoDeBitacora(self, usuario, identificador):
        # copiar estado previo en la bitacora (no vigente) y
        # actualizar estado de elemento de bitacora
        self.bitacorarElemento(usuario, identificador)
        

class TUForm(BitacoraForm):
    class Meta:
        model = TipoUsuario
        fields = [
            'nombre',
            'descripcion',
            'cantidad',
            'usuariosContactables',
        ]

class RUForm(BitacoraForm):
    def __init__(self,*args,**kwargs):
        super (RUForm,self).__init__(*args,**kwargs)
        self.camposVigentesDelProyecto = [
            'tiposUsuario',
            'hito',
        ]
        
    class Meta:
        model = RequisitoUsuario
        
        fields = [
            'nombre',
            'descripcion',
            'fuente',
            'costo',
            'estabilidad',
            'tipo',
            'prioridad',
            'estado',
            'tiposUsuario',
            'hito',
        ]

class RSForm(BitacoraForm):
    def __init__(self,*args,**kwargs):
        super (RSForm,self).__init__(*args,**kwargs)
        self.camposVigentesDelProyecto = [
            'tiposUsuario',
            'requisitosUsuario',
            'hito',
        ]
    
    class Meta:
        model = RequisitoSoftware
        fields = [
            'nombre',
            'descripcion',
            'fuente',
            'costo',
            'estabilidad',
            'tipo',
            'prioridad',
            'estado',
            'tiposUsuario',
            'requisitosUsuario',
            'hito',
        ]
        
class CPForm(BitacoraForm):
    def __init__(self,*args,**kwargs):
        super (CPForm,self).__init__(*args,**kwargs)
        self.camposVigentesDelProyecto = [
            'tiposUsuario',
            'requisitoSoftware',
            'requisitoUsuario',
        ]
    
    class Meta:
        model = CasoPrueba
        fields = [
            'nombre',
            'requisitoSoftware',
            'requisitoUsuario',
            'descripcion',
            'resultadoAceptable',
            'resultadoOptimo',
            'tiposUsuario',
            'estado',
        ]
        
class MDForm(BitacoraForm):
    def __init__(self,*args,**kwargs):
        super (MDForm,self).__init__(*args,**kwargs)
        self.camposVigentesDelProyecto = [
            'requisitosSoftware',
        ]
    
    class Meta:
        model = Modulo
        fields = [
            'nombre',
            'descripcion',
            'requisitosSoftware',
            'costo',
            'prioridad',
            
        ]
