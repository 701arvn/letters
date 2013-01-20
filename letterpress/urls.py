from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from lpapp import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(
        regex=r"^$",
        view=views.MessageListView.as_view(),
    ),
    url(r'^create_message', 'lpapp.views.create_message', name='create_message'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
