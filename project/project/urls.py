from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from project import settings


urlpatterns = patterns('',
    url(r'^$', 'project.views.home', name='home'),
    url(r'^translate/', 'project.views.translate', name='translate'),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
              static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
