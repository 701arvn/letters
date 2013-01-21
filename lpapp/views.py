from hashlib import md5
from datetime import datetime
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse
from django.conf import settings
from models import *


class MessageListView(generic.ListView):
    template_name = "message_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(MessageListView, self).get_context_data(*args, **kwargs)
        context['session_id'] = self.kwargs['session_id']
        context['async_url'] = settings.ASYNC_BACKEND_URL
        return context

    def get_queryset(self):
        return Message.objects.filter(session_id=self.kwargs['session_id'])[:10]


@login_required
def main_view(request):
    session_id = md5(str(datetime.now()) + request.user.username).hexdigest()
    return redirect('session_view', session_id=session_id)


def create_message(request):
    m = Message(
        user=request.user,
        text=request.POST['message_text'],
        session_id=request.POST['session_id'])
    try:
        m.save()
    except Exception as e:
        print str(e)
    return HttpResponse("OK")
