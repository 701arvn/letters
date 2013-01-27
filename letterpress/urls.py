from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

# Uncomment the next two lines to enable the admin:
from lpmessage import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login'),
    url(r'^$', 'lpmessage.views.main_view'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^mongonaut/', include('mongonaut.urls')),

    url(r'^game/$', 'lpgame.views.main_game_view'),
    url(r"^game/(?P<session_id>\w+)/$", 'lpgame.views.game_view',
        name='new_game_view'
    ),

    url(
        regex=r"^(?P<session_id>\w+)/$",
        view=login_required(views.MessageListView.as_view()),
        name='message_view'
    ),

    url(r'^create_message', 'lpmessage.views.create_message', name='create_message'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
)
