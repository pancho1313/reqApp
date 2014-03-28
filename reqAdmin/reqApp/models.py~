# -*- encoding: utf-8 -*-
from django.db import models
from django.db.models import Max
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from reqApp.choices import *
from django.utils import timezone

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
    """
    def get_queryset(self):
        return super(BitacoraManager, self).get_queryset().filter(vigencia=True)
    
        
    def todos(self, proyecto):
        return super(BitacoraManager, self).get_queryset().filter(proyecto=proyecto)
        
    """
    def vigentes(self, proyecto, order='identificador'):
        return self.model.objects.filter(proyecto=proyecto).filter(vigencia=True).order_by(order)
        
    def vigente(self, proyecto, identificador):
        try:
            resp = self.model.objects.filter(proyecto=proyecto).filter(vigencia=True).filter(identificador=identificador)[:1].get()
        except self.model.DoesNotExist:
            resp = None
        return resp
    
    def nuevoIdentificador(self, proyecto):
        elementos = self.model.objects.all().filter(proyecto=proyecto)
        
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
    """
    def m2mVigentes(self):
        # aca se crea un diccionario con referencias m2m que son vigentes
        return {}
    def copiarM2MVigentes(self, m2mVigentesDicc):
        # aca se realiza la copia de las referencias m2m que son vigentes
        pass
    """ 
    
    def bitacorarCopiaDeElemento(self, proyecto, identificador):
        # registrar una copia no vigente en la bitacora
        elementoPrevio = self.__class__.objects.vigente(proyecto, identificador)
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
    
    def bitacorarElemento(self, usuario):
        #registrar usuario responsable
        self.usuario = usuario
        
        # fecha de creación / modificación
        self.fecha = timezone.now()
        
        # guardar en base de datos
        self.save()
     
    def bitacorarNuevoElemento(self, proyecto, usuario):
        # identificador nuevo
        self.identificador = self.__class__.objects.nuevoIdentificador(proyecto)
        
        # vigencia del elemento
        self.vigencia = True
        
        # proyecto asociado
        self.proyecto = proyecto
        
        # guardar en base de datos
        self.bitacorarElemento(usuario)

    def bitacorarElementoBorrado(self, usuario):
        # registrar una copia no vigente en la bitacora
        self.bitacorarCopiaDeElemento(self.proyecto, self.identificador)
        
        # un elemento borrado no es vigente
        self.vigencia = False
        
        # guardar en base de datos
        self.bitacorarElemento(usuario)
    
    def campos(self):
        return [
            self.identificador,
            self.nombre,
            self.descripcion,
        ]

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
    
    def campos(self):
        return Bitacora.campos(self) + [
            self.cantidad,
            self.usuariosContactables,
        ]
    

    
class RequisitoUsuario(Bitacora):
    fuente = models.CharField(max_length=140, blank=True)
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
    
    def m2mVigentes(self):
        # aca se crea un diccionario con referencias m2m que son vigentes
        print self.tiposUsuario.all()
        print self.tiposUsuario.filter(vigencia=True)
        return {
            'tiposUsuario':self.tiposUsuario.filter(vigencia=True),
        }
        
    def copiarM2MVigentes(self, m2mVigentesDicc):
        # aca se realiza la copia de las referencias m2m que son vigentes
        self.tiposUsuario = m2mVigentesDicc['tiposUsuario']
    
    def campos(self):
        return Bitacora.campos(self) + [
            self.estado,
            self.fuente,
            self.costo,
            self.estabilidad,
            self.tipo,
            self.prioridad,
            self.tiposUsuario,
            self.hito,
        ]
    
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
