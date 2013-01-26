from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import urllib2
import urllib
import json
from mongoengine import *


class EnglishWords(Document):
    word_id = IntField()
    word = StringField(max_length=30)


class Letter(EmbeddedDocument):
    letter_id = IntField()
    letter = StringField(max_length=1)


class PlayedWords(EmbeddedDocument):
    gamer = IntField()
    words = ListField(StringField(max_length=30))


class PlayedLetters(EmbeddedDocument):
    gamer = IntField()
    letters = ListField(EmbeddedDocumentField(Letter))


class Game(Document):
    gamers = ListField(IntField())
    played_words = ListField(EmbeddedDocumentField(PlayedWords))
    letters = ListField(EmbeddedDocumentField(Letter))
    played_letters = ListField(EmbeddedDocumentField(PlayedLetters))
    session_id = StringField(max_length=20)



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


def send_event(event_type, event_data, session_id):
    to_send = {
        'event': event_type,
        'data': event_data,
        'session_id': session_id,
    }
    urllib2.urlopen(settings.ASYNC_BACKEND_URL, urllib.urlencode(to_send))
