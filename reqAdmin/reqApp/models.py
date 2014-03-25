from django.db import models
from django.db.models import Max
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from reqApp.choices import *

class Proyecto(models.Model):
    nombre = models.CharField(max_length=64)
    descripcion = models.CharField(max_length=140)
    
    def __unicode__(self):
        return u'%s' % self.nombre

class UserProfile(models.Model):
    """
    >>> u = User.objects.get(username='fred')
    >>> freds_proyecto = u.userProfile.proyectos
    """
    user = models.OneToOneField(User)
    
    # un usuario debe escoger el proyecto que desea ver (en el caso de tener mas de uno asociado)
    proyectos = models.ManyToManyField(Proyecto, null=True)
    
def profile(sender, **kwargs):
    if kwargs.get('created', False):
        UserProfile.objects.create(
            user=kwargs.get('instance')
            )
post_save.connect(profile, sender=User)

class BitacoraManager(models.Manager):
    def todos(self, proyecto_id):
        try:
            resp = self.model.objects.filter(proyecto__id=proyecto_id)
        except self.model.DoesNotExist:
            pass
        return resp
        
        
    def vigentes(self, proyecto_id):
        try:
            resp = self.model.objects.filter(proyecto__id=proyecto_id).filter(vigencia=True)
        except self.model.DoesNotExist:
            pass
        return resp
        
    def vigente(self, identificador):
        try:
            resp = self.model.objects.filter(proyecto__id=proyecto_id).filter(vigencia=True)
        except self.model.DoesNotExist:
            pass
        return resp
    
    def nuevoIdentificador(self):
        elementos = self.model.objects.all()
        
        if elementos.count() > 0:
            return elementos.aggregate(Max('identificador'))['identificador__max'] + 1
        return 1

class Bitacora(models.Model):
    nombre = models.CharField(max_length=64)
    identificador = models.PositiveIntegerField(default=0, blank=True, null=False)
    descripcion = models.CharField(max_length=200, blank=True)
    proyecto = models.ForeignKey(Proyecto, blank=True, null=False)
    fecha = models.DateTimeField()
    usuario = models.ForeignKey(User, null=True) # TODO referenciar al User correcto
    vigencia = models.BooleanField()
    
    def __unicode__(self):
        return u'%s' % self.nombre
        


class Hito(Bitacora):
    fechaInicio = models.DateTimeField()
    fechaFin = models.DateTimeField()
    
    objects = BitacoraManager()
    
class TipoUsuario(Bitacora):
    cantidad = models.PositiveIntegerField(default=1)
    usuariosContactables = models.CharField(max_length=140) # TODO en realidad es mejor una lista
    
    objects = BitacoraManager()
    
    def __unicode__(self):
        return u'TU%04d %s' % (self.identificador, self.nombre)
    

    
class RequisitoUsuario(Bitacora):
    fuente = models.CharField(max_length=140)
    costo = models.IntegerField(default=0, blank=True)
    
    estabilidad = models.CharField(max_length=30, choices=ESTABILIDAD_CHOICES)
    tipo = models.CharField(max_length=30, choices=TIPO_RU_CHOICES)
    prioridad = models.CharField(max_length=30, choices=PRIORIDAD_CHOICES)
    estado = models.CharField(max_length=30, choices=ESTADO_CHOICES)
    
    tiposUsuario = models.ManyToManyField(TipoUsuario, null=True, blank=True)
    hito = models.ForeignKey(Hito, blank=False, null=False)
    
    objects = BitacoraManager()
    
    def __unicode__(self):
        return u'RU%04d %s' % (self.identificador, self.nombre)
    
class RequisitoSoftware(Bitacora):
    fuente = models.CharField(max_length=140)
    costo = models.IntegerField(default=0, blank=True)
    
    estabilidad = models.CharField(max_length=30, choices=ESTABILIDAD_CHOICES)
    tipo = models.CharField(max_length=30, choices=TIPO_RS_CHOICES)
    prioridad = models.CharField(max_length=30, choices=PRIORIDAD_CHOICES)
    estado = models.CharField(max_length=30, choices=ESTADO_CHOICES)
    
    tiposUsuario = models.ManyToManyField(TipoUsuario, null=True, blank=True)
    requisitosUsuario = models.ManyToManyField(RequisitoUsuario, null=True, blank=True)
    hito = models.ForeignKey(Hito, blank=False, null=False)
    
    objects = BitacoraManager()
    
    def __unicode__(self):
        return u'RS%04d %s' % (self.identificador, self.nombre)

class CasoPrueba(Bitacora):
    resultadoAceptable = models.CharField(max_length=140)
    resultadoOptimo = models.CharField(max_length=140)
    
    estado = models.CharField(max_length=30, choices=ESTADO_CHOICES)
    
    tiposUsuario = models.ManyToManyField(TipoUsuario, null=True, blank=True)
    requisitoSoftware = models.ForeignKey(RequisitoSoftware, null=True, blank=True)
    requisitoUsuario = models.ForeignKey(RequisitoUsuario, null=True, blank=True)
    
    objects = BitacoraManager()
    
    def __unicode__(self):
        return u'CP%04d %s' % (self.identificador, self.nombre)
        
class Modulo(Bitacora):
    costo = models.IntegerField(default=0, blank=True)
    
    prioridad = models.CharField(max_length=30, choices=PRIORIDAD_CHOICES)
    
    requisitosSoftware = models.ManyToManyField(RequisitoSoftware, null=True, blank=True)
    
    objects = BitacoraManager()
    
    def __unicode__(self):
        return u'MD%04d %s' % (self.identificador, self.nombre)
