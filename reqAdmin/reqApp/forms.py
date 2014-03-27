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
        
    def bitacorarElemento(self, usuario, identificador=None, borrar=False):
        elemento = self.save(commit=False)
        
        if identificador == None: # crear un elemento nuevo
            # identificador nuevo
            elemento.identificador = elemento.__class__.objects.nuevoIdentificador(self.proyecto)
            
            # vigencia del elemento
            elemento.vigencia = True
            
            # obtener el proyecto asociado
            elemento.proyecto = self.proyecto
            
        else: # editar elemento
            # registrar una copia no vigente en la bitacora
            elementoPrevio = elemento.__class__.objects.vigente(self.proyecto, identificador)
            if elementoPrevio == None:
                # TODO: ERROR
                print "ERROR"
            # https://docs.djangoproject.com/en/1.6/topics/db/queries/#copying-model-instances
            m2mVigentes = elementoPrevio.m2mVigentes()
            elementoPrevio.id = None # para luego crear un registro nuevo en la bitacora
            elementoPrevio.pk = None # para luego crear un registro nuevo en la bitacora
            elementoPrevio.save() # obtener nuevo id para el nuevo registro
            elementoPrevio.copiarM2MVigentes(m2mVigentes)
            elementoPrevio.vigencia = False
            elementoPrevio.save() # guardar el estado del elemento previo
        
        # obtener usuario
        elemento.usuario = usuario
        
        # fecha de creación
        elemento.fecha = timezone.now()
        
        if borrar: # borrar el elemento cuenta como una edicion actualizando un elemento a no-vigente
            elemento.vigencia = False
        
        # guardar elemento de bitacora
        elemento.save()
        
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
        super (RUForm,self ).__init__(*args,**kwargs)
        self.camposVigentesDelProyecto = [
            'tiposUsuario',
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
