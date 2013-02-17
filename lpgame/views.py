import math
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.conf import settings
from django.http import HttpResponse
from base import get_uniq_hash
from models import *


@login_required
def main_game_view(request):
    session_id = get_uniq_hash(request)
    generate_game(request.user, session_id)
    return redirect('new_game_view', session_id=session_id)


@login_required
def game_view(request, session_id):
    game = Game.objects.get(session_id=session_id)
    if request.user.pk not in game.gamers:
        game.gamers.append(request.user.pk)
    letters_in_row = int(math.sqrt(len(game.letters)))
    variables = {
        'session_id': session_id,
        'async_url': settings.ASYNC_BACKEND_URL,
        'letters': game.to_mongo()['letters'],
        'letters_in_row': letters_in_row,
        'rows_range': xrange(letters_in_row)
    }
    return render(request, 'lpgame/game.html', variables)


def make_turn(request):
    session_id = request.POST.get('session_id')
    selected_letters = request.POST.getlist('selected[]')
    game = Game.objects.get(session_id=session_id)
    word = ''
    for letter_entry in selected_letters:
        letter_id = int(letter_entry.split('_')[1])  # TODO do it in javascript
        letter = get_letter_by_id(game, letter_id)
        word += letter
    print word
    return HttpResponse("OK")
