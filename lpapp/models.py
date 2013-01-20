from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    user = models.ForeignKey(User, null=True)
    text = models.TextField(u"text")
    created_at = models.DateTimeField(u"created at", auto_now_add=True)
