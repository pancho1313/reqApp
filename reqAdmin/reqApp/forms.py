# -*- encoding: utf-8 -*-
from django import forms
from reqApp.models import *
from django.utils import timezone

from tinymce.widgets import TinyMCE

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
        widgets = {
            'descripcion': forms.Textarea(attrs={'cols': 100, 'rows': 4}),
            'nombre': forms.TextInput(attrs={'size': 80}),
            'cantidad': forms.TextInput(attrs={'size': 5}),
            'usuariosContactables': forms.Textarea(attrs={'cols': 50, 'rows': 4}),
        }

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
        
        widgets = {
            'descripcion': forms.Textarea(attrs={'cols': 100, 'rows': 4}),
            'nombre': forms.TextInput(attrs={'size': 80}),
        }

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
        
        widgets = {
            'descripcion': forms.Textarea(attrs={'cols': 100, 'rows': 4}),
            'nombre': forms.TextInput(attrs={'size': 80}),
        }
        
class CPForm(BitacoraForm):
    def __init__(self,*args,**kwargs):
        super (CPForm,self).__init__(*args,**kwargs)
        self.camposVigentesDelProyecto = [
            'tiposUsuario',
        ]
    
    def asignarProyecto(self, proyecto):
        self.proyecto = proyecto
        
        # estos campos solo consideran elementos vigentes del proyecto ordenados por identificador
        for campo in self.camposVigentesDelProyecto:
            self.fields[campo].queryset = self.fields[campo].queryset.filter(vigencia=True).filter(proyecto=self.proyecto).order_by('identificador')
            
        self.fields['requisito'].queryset = self.fields['requisito'].queryset.filter(vigencia=True).filter(proyecto=self.proyecto).order_by('requisitousuario')
            
        return self
    
    class Meta:
        model = CasoPrueba
        fields = [
            'nombre',
            'requisito',
            'descripcion',
            'resultadoAceptable',
            'resultadoOptimo',
            'tiposUsuario',
            'estado',
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'cols': 100, 'rows': 4}),
            'nombre': forms.TextInput(attrs={'size': 80}),
            'resultadoAceptable': forms.Textarea(attrs={'cols': 70, 'rows': 2}),
            'resultadoOptimo': forms.Textarea(attrs={'cols': 70, 'rows': 2}),
        }
        
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
        widgets = {
            'descripcion': forms.Textarea(attrs={'cols': 100, 'rows': 4}),
            'nombre': forms.TextInput(attrs={'size': 80}),
        }
        
class HTForm(BitacoraForm):
    
    class Meta:
        model = Hito
        fields = [
            'nombre',
            'descripcion',
            'fechaInicio',
            'fechaFin',
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'cols': 100, 'rows': 4}),
            'nombre': forms.TextInput(attrs={'size': 80}),
        }
        
        

# TinyMCE
class FlatPageForm(forms.ModelForm):
    """
    theme_advanced_buttons1 : "bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,styleselect,formatselect,|,forecolor,backcolor",
	theme_advanced_buttons2 : "bullist,numlist,|,outdent,indent,|,undo,redo,|,link,unlink,anchor,image,cleanup,help,code",
	theme_advanced_buttons3 : "hr,removeformat,visualaid,|,sub,sup,|,charmap"
	theme_advanced_path : true,
    theme_advanced_toolbar_location : 'top',
    theme_advanced_blockformats : "p,address,pre,h1,h2,h3,h4,h5,h6",
    theme_advanced_toolbar_align : "left",
    theme_advanced_statusbar_location : "bottom",
    """
    class Meta:
        model = MCEModel
        fields = [
            'my_mce',
        ]
        widgets = {
            'my_mce': TinyMCE(
                attrs={'cols': 80, 'rows': 30},
                mce_attrs={
                    'theme':'advanced',
                    'plugins':'yenimg',
                    'theme_advanced_statusbar_location':None,
                    'theme_advanced_blockformats':"p,h2,h3,h4,h5,h6",
                    'theme_advanced_buttons1':
                        "formatselect,|,bold,italic,underline,|,justifyleft,justifycenter,justifyright,justifyfull,|,outdent,indent,|,bullist,numlist,|,imgurl,browseimg,|,undo,redo",
                    'theme_advanced_buttons2':"",
                    'theme_advanced_buttons3':"",
                    })
        }
"""
# redactor
class RedactorForm(forms.ModelForm):
    class Meta:
        model=RedactorModel
        fields = [
            'short_text',
        ]
"""

class DocForm(forms.ModelForm):
    def registrarDocumento(self, proyecto, usuario, tipoParrafo):
        (self.save(commit=False)).registrarDocumento(proyecto, usuario, tipoParrafo)
        
    class Meta:
        model=Documento
        fields = [
            'parrafo',
        ]

class MceImageForm(forms.Form):
    file = forms.ImageField()
