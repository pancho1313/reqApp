from django import forms
from reqApp.models import *

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre', 'descripcion']
        
class HitoForm(forms.ModelForm):
    class Meta:
        model = Hito
        fields = ['nombre', 'descripcion']
        # TODO
