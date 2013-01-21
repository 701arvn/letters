from django.views import generic
from django.http import HttpResponse
from models import *


class MessageListView(generic.ListView):
    queryset = Message.objects.all()[:10]
    template_name = "message_list.html"


def create_message(request):
    if request.user.is_anonymous():
        user = None
    else:
        user = request.user
    m = Message(user=user, text=request.POST['message_text'])
    try:
        m.save()
    except Exception as e:
        print str(e)
    return HttpResponse("OK")
