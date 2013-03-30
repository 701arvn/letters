import math
import json
import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.conf import settings
from django.http import HttpResponse, Http404
from base import get_uniq_hash
from models import *

logger = logging.getLogger('lpgame')


@login_required
def main_game_view(request):
    session_id = get_uniq_hash(request)
    generate_game(request.user, session_id)
    logger.info("the game {} has started by {}".format(
        session_id,
        request.user.username
    ))
    return redirect('new_game_view', session_id=session_id)


@login_required
def game_view(request, session_id):
    # TODO check if game ended
    game = Game.objects.get(session_id=session_id)
    if request.user.pk not in game.gamers:
        if len(game.gamers) == game.MAX_GAMERS:
            logger.debug("too many gamers in game {}".format(session_id))
            raise Http404
        game.gamers.append(request.user.pk)
        game.save()
    letters = game.letters
    rows_count = int(math.sqrt(len(letters)))
    rows = []
    for i in xrange(rows_count):
        rows.append(letters[i * rows_count: i * rows_count + rows_count])

    variables = {
        'session_id': session_id,
        'async_url': settings.ASYNC_BACKEND_URL,
        'rows': rows,
        'user_id': request.user.pk,
        'is_current_player': game.is_current_player(request.user.pk)
    }
    return render(request, 'lpgame/game.html', variables)


def make_turn(request):
    # TODO check if game ended
    session_id = request.POST.get('session_id')
    selected_letters = request.POST.getlist('selected[]')
    letters = [int(entry) for entry in selected_letters]
    game = Game.objects.get(session_id=session_id)
    word = ''
    for letter_id in letters:
        letter = get_letter_by_id(game, int(letter_id))
        word += letter.letter
    try:
        send_event_on_user_turn(game, word, letters, request.user)
    except WordAlreadyUsedException:
        return HttpResponse(
            json.dumps(
                {'success': False, 'error': "Word already used", 'code': 1}
            ),
            mimetype="application/json"
        )
    except NotAWordException:
        return HttpResponse(
            json.dumps(
                {'success': False, 'error': "Not a word", 'code': 2}
            ),
            mimetype="application/json"
        )
    except Exception as exc:
        logger.exception('problem in processing turn')
        raise Http404
    return HttpResponse(json.dumps({'success': True}), mimetype="application/json")


def end_game(request):
    session_id = request.POST.get('session_id')
    game = Game.objects.get(session_id=session_id)
    game.end()
    send_event('game_ended', {}, game.session_id)
    return HttpResponse(json.dumps({'success': True}), mimetype="application/json")
