# -*- encoding: utf-8 -*-
from django import forms
from reqApp.models import *
from django.utils import timezone

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre', 'descripcion']

class BitacoraForm(forms.ModelForm):
    def crearElementoDeBitacora(self, usuario):
        elemento = self.save(commit=False)
        
        # obtener usuario
        elemento.usuario = usuario
        
        # obtener el proyecto asociado
        elemento.proyecto = Proyecto.objects.all()[:1].get() # TODO obtener proyecto del usuario
        
        # fecha de creación
        elemento.fecha = timezone.now()
        
        # identificador nuevo
        elemento.identificador = elemento.__class__.objects.nuevoIdentificador()
        elemento.vigencia = True
        
        # guardar elemento de bitacora
        elemento.save()
        
        # actualizar relaciones "many2many"
        self.save_m2m()

class TUForm(BitacoraForm):
    class Meta:
        model = TipoUsuario
        fields = [
            'nombre',
            'descripcion',
            'cantidad',
            'usuariosContactables',
        ]
