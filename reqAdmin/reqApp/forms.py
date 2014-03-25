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
        # TODO obtener proyecto seleccionado de sesion de usuario
        # por el momento seleccionamos siempre el "primer" proyecto asociado al usuario
        elemento.proyecto = usuario.userprofile.proyectos.all()[:1].get()
        
        # fecha de creación
        elemento.fecha = timezone.now()
        
        # identificador nuevo
        elemento.identificador = elemento.__class__.objects.nuevoIdentificador()
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
