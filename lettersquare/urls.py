from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'lpgame.views.main_page'),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login'),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^mongonaut/', include('mongonaut.urls')),
    url(r'^message/', include('lpmessage.urls')),
    url(r'^game/', include('lpgame.urls')),
    url(r'', include('social_auth.urls')),
)
if not settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )