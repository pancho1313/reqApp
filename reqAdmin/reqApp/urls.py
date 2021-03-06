from django.conf.urls import patterns, url

from reqApp import views

urlpatterns = patterns('',
    url(r'^$' , 'django.contrib.auth.views.login',
        {'template_name':'reqApp/index.html'}, name='login'),
    url(r'^logout/$' , 'django.contrib.auth.views.logout_then_login',
        name='logout'),

    url(r'^proyecto/$', views.selectProject, name='PR'),

    url(r'^proyecto/TU/$', views.viewTU, name='TU'),
    url(r'^proyecto/RU/$', views.viewRU, name='RU'),
    url(r'^proyecto/RS/$', views.viewRS, name='RS'),
    url(r'^proyecto/MD/$', views.viewMD, name='MD'),
    url(r'^proyecto/CP/$', views.viewCP, name='CP'),
    url(r'^proyecto/HT/$', views.viewHT, name='HT'),
    
    url(r'^documentos/requisitos/$', views.docRequisitos, name='docReq'),
    url(r'^documentos/diseno/$', views.docDiseno, name='docDis'),
    url(r'^documentos/casos_de_prueba/$', views.docCP, name='docCP'),
    url(r'^documentos/historico/$', views.docHistorico, name='docHis'),
    
    url(r'^herramientas/tareas/$', views.tareas, name='tareas'),
    url(r'^herramientas/estadisticas/$', views.estadisticas, name='estadisticas'),
    url(r'^herramientas/matrices/$', views.matrices, name='matrices'),
    url(r'^herramientas/consistencia/$', views.consistencia, name='consistencia'),
    url(r'^herramientas/bitacora/$', views.bitacora, name='bitacora'),
    
    url('^upload/img/$', views.imgUpload, name='mce_upload_image'),
    
    url(r'pdf/$', views.pdf, name='pdf'),
    
    url(r'^ayuda/$', views.help, name='help'),
)
