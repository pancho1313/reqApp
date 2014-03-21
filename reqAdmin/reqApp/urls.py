from django.conf.urls import patterns, url

from reqApp import views

urlpatterns = patterns('',
    url(r'^TU/$', views.viewTU, name='TU'),
    url(r'^RU/$', views.viewRU, name='RU'),
    url(r'^RS/$', views.viewRS, name='RS'),
    url(r'^MD/$', views.viewMD, name='MD'),
    url(r'^CP/$', views.viewCP, name='CP'),
)
