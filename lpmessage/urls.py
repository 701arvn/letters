from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from lpmessage import views


urlpatterns = patterns('',
    url(r'^$', 'lpmessage.views.main_view'),
    url(
        regex=r"^(?P<session_id>\w+)/$",
        view=login_required(views.MessageListView.as_view()),
        name='message_view'
    ),
    url(r'^create_message', 'lpmessage.views.create_message', 
                                name='create_message'),
)
