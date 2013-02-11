from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'lpgame.views.main_game_view'),
    url(r'^make_turn/$', 'lpgame.views.make_turn'),
    url(r"^(?P<session_id>\w+)/$", 'lpgame.views.game_view',
        name='new_game_view'
    ),
)
