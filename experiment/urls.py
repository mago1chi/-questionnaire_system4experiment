from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'experiment.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^evaluate/', include('evaluate.urls', namespace="evaluate")),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
