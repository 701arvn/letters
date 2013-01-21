from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

# Uncomment the next two lines to enable the admin:
from lpapp import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login'),
    url(r'^$', 'lpapp.views.main_view'),
    url(r'^admin/', include(admin.site.urls)),
    url(
        regex=r"^(?P<session_id>\w+)/$",
        view=login_required(views.MessageListView.as_view()),
        name='session_view'
    ),

    url(r'^create_message', 'lpapp.views.create_message', name='create_message'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
)
