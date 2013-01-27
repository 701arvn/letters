from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^mongonaut/', include('mongonaut.urls')),
    url(r'^message/', include('lpmessage.urls')),
    url(r'^game/', include('lpgame.urls')),
)
