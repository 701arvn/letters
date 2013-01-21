from django.db import models
from django.contrib.auth.models import User
import urllib2
import urllib
import json


class Message(models.Model):
    user = models.ForeignKey(User, null=True)
    text = models.TextField(u"text")
    created_at = models.DateTimeField(u"created at", auto_now_add=True)

    def __unicode__(self):
        return "%s" % (self.text,)

    def as_dict(self):
        data = {
            'id': self.pk,
            'text': self.text,
        }
        return json.dumps(data)

    def save(self, *args, **kwargs):
        uniq_id = kwargs.pop('uniq_id')
        super(Message, self).save(*args, **kwargs)
        send_event('message-create', self.as_dict(), uniq_id)


def send_event(event_type, event_data, uniq_id):
    to_send = {
        'event': event_type,
        'data': event_data,
        'uniq_id': uniq_id,
    }
    urllib2.urlopen('http://localhost:8001', urllib.urlencode(to_send))
