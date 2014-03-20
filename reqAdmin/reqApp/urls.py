from django.conf.urls import patterns, url

from reqApp import views

urlpatterns = patterns('',
    url(r'^$', views.test, name='test'),
    """
    url(r'^(?P<poll_id>\d+)/$', views.detail, name='detail'),
    url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
    url(r'^(?P<poll_id>\d+)/results/$', views.results, name='results'),
    """
)
