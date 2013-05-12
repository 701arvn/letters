# coding: utf-8
from django import template
from django.contrib.auth.models import User
from ..models import Game


register = template.Library()


@register.simple_tag(takes_context=True)
def game_score(context):
    users = _game_users(context)
    if len(users) < 2:
        return ""
    game = context['game']
    game_score = game.score()
    return u"<b>{}</b> – <b>{}</b>".format(
        game_score[users[0]],
        game_score[users[1]],
    )


@register.simple_tag(takes_context=True)
def game_users(context):
    users = _game_users(context)
    if len(users) < 2:
        return User.objects.get(pk=users[0]).get_full_name()
    return u"{} – {}".format(
        User.objects.get(pk=users[0]).get_full_name(),
        User.objects.get(pk=users[1]).get_full_name(),
    )


@register.simple_tag(takes_context=True)
def current_score(context):
    users = _game_users(context)
    if len(users) < 2:
        return ""
    game = context['game']
    game_score = game.score()
    # TODO do it another way
    return u"""<div class="user" id="name_user1">{user1}</div> <div class="score" id="score_user1">{score1}</div> – <div class="score" id="score_user2">{score2}</div> <div class="user" id="name_user2">{user2}</div>""".format(
        score1=game_score[users[0]],
        score2=game_score[users[1]],
        user1=User.objects.get(pk=users[0]).get_full_name(),
        user2=User.objects.get(pk=users[1]).get_full_name(),
    )


def _game_users(context):
    game = context['game']
    game_score = game.score()
    keys = game_score.keys()
    if len(keys) < 2:
        return keys
    users = []
    # THIS IS REAL SHIT
    for key in keys:
        if key == context['user'].pk:
            users.append(key)
            keys.remove(key)
            users.append(keys[0])
            break
    return users


