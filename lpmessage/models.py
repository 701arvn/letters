import json
from django.db import models
from django.contrib.auth.models import User
from base import send_event


class Message(models.Model):
    user = models.ForeignKey(User, null=True)
    text = models.TextField(u"text")
    created_at = models.DateTimeField(u"created at", auto_now_add=True)
    session_id = models.CharField(max_length=100)

    def __unicode__(self):
        return "%s" % (self.text,)

    class Meta:
        ordering = ('-id',)

    def as_dict(self):
        data = {
            'id': self.pk,
            'text': self.text,
            'user': self.user.username,
        }
        return json.dumps(data)

    def save(self, *args, **kwargs):
        super(Message, self).save(*args, **kwargs)
        send_event('message-create', self.as_dict(), self.session_id)
