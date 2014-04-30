from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

#from filebrowser.sites import site

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'reqAdmin.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('reqApp.urls', namespace="reqApp")),
    #url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^tinymce/', include('tinymce.urls')),
    url(r'^redactor/', include('redactor.urls')),
)
