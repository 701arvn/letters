from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import string
import random
import urllib2
import urllib
import json
from mongoengine import *


class EnglishWords(Document):
    WORDS_COUNT = 60388

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


def clean_list(letters):
    for letter in string.ascii_lowercase:
        if letters.count(letter) >= 3 and len(letters) > 25:
            letters.remove(letter)
    if len(letters) > 25:
        letters = letters[:25]
    return letters


def generate_letters():
    letters = []
    while len(letters) <= 25:
        word_id = random.randint(1, EnglishWords.WORDS_COUNT)
        word = EnglishWords.objects.get(word_id=word_id).word
        letters += list(word)
    random.shuffle(letters)
    letters = clean_list(letters)
    return letters


def generate_game(user, session_id):
    game = Game(gamers=[user.pk], session_id=session_id)
    letters = generate_letters()
    for i, letter in enumerate(letters):
        game.letters.append(Letter(letter_id=i + 1, letter=letter))
    game.save()


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
