from django.conf.urls import patterns, include, url

from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from filebrowser.sites import site

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'reqAdmin.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('reqApp.urls', namespace="reqApp")),
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tinymce/', include('tinymce.urls')),
    #url(r'^redactor/', include('redactor.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': False}),
)
