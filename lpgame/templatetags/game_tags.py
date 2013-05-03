# coding: utf-8
from django import template
from django.contrib.auth.models import User
from ..models import Game


register = template.Library()


@register.simple_tag(takes_context=True)
def game_score(context):
    game = context['game']
    game_score = game.score()
    keys = game_score.keys()
    if len(keys) < 2:
        return ""
    users = []
    # THIS IS REAL SHIT
    for key in keys:
        if key == context['user'].pk:
            users.append(key)
            keys.remove(key)
            users.append(keys[0])
            break
    # TODO check if current
    return u"<p>{} <b>{}</b> – <b>{}</b> {}</p>".format(
        User.objects.get(pk=users[0]).username,
        game_score[users[0]],
        game_score[users[1]],
        User.objects.get(pk=users[1]).username,
    )


