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
        
        # estos campos solo consideran elementos vigentes del proyecto
        
        for campo in self.camposVigentesDelProyecto:
            self.fields[campo].queryset = self.fields[campo].queryset.filter(vigencia=True).filter(proyecto=self.proyecto)
        return self
        
    def crearElementoDeBitacora(self, usuario):
        elemento = self.save(commit=False)
        
        # obtener usuario
        elemento.usuario = usuario
        
        # obtener el proyecto asociado
        elemento.proyecto = self.proyecto
        
        # fecha de creación
        elemento.fecha = timezone.now()
        
        # identificador nuevo
        elemento.identificador = elemento.__class__.objects.nuevoIdentificador(self.proyecto)
        elemento.vigencia = True
        
        # guardar elemento de bitacora
        elemento.save()
        
        # actualizar relaciones "many2many"
        self.save_m2m()
    
    def actualizarElementoDeBitacora(self, identificador, usuario):
        # TODO
        pass

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
