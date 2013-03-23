import random
import string
import urllib2
import urllib
import logging
from django.conf import settings

from mongoengine import *

logger = logging.getLogger('lpgame')

class EnglishWords(Document):
    WORDS_COUNT = 60388

    word_id = IntField()
    word = StringField(max_length=30)

    @staticmethod
    def is_a_word(word):
        result = EnglishWords.objects(word=word).first()
        return result is not None


class Letter(EmbeddedDocument):
    letter_id = IntField()
    letter = StringField(max_length=1)
    gamer = IntField()


class PlayedWords(EmbeddedDocument):
    gamer = IntField()
    words = ListField(StringField(max_length=30))


class Game(Document):
    MAX_GAMERS = 2
    ended = BooleanField(default=False)
    gamers = ListField(IntField())
    played_words = ListField(EmbeddedDocumentField(PlayedWords))
    letters = ListField(EmbeddedDocumentField(Letter))
    session_id = StringField(max_length=20)
    current_player = IntField()
    winner_id = IntField()

    def end(self):
        self.ended = True
        self.save()

    def is_current_player(self, user_id):
        return user_id == self.current_player
 
    def change_current_player(self):
        for gamer in self.gamers:
            if self.is_current_player(gamer):
                continue
            else:
                self.current_player = gamer
                break
        self.save()

    def is_all_letters_played(self):
        counter = 0
        for letter in self.letters:
            if letter.gamer is not None:
                counter += 1
        return counter == len(self.letters)

    @property
    def winner(self):
        if not self.ended:
            raise Exception("No winner. Game in process")
        if self.winner_id is not None:
            return self.winner_id
        res = {x:0 for x in self.gamers}
        for letter in self.letters:
            res[letter.gamer] += 1
        self.winner_id = max(res.iterkeys(), key=lambda k: res[k])
        self.save()
        return self.winner_id


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
    game.current_player = user.pk
    game.save()
    return game


def get_letter_by_id(game, letter_id):
    for letter in game.letters:
        if letter.letter_id == letter_id:
            return letter
    raise DoesNotExist('No such letter')


def send_event_on_successful_turn(game, word, letters, user):
    letters_to_send = on_successful_turn(game, word, letters, user)
    logger.debug("{} played word '{}' in game {}".format(
        user.username,
        word,
        game.session_id
    ))
    send_event('new_turn', letters_to_send, game.session_id, user.pk)
    if game.is_all_letters_played():
        game.end()
        logger.info("game {} has ended, the winner is {}".format(
            game.session_id,
            user.username
        ))
        send_event('game_over', {'winner': game.winner}, game.session_id)


def on_successful_turn(game, word, letters, user):
    user_words = None
    for played_words in game.played_words:
        if word in played_words.words:
            raise Exception('Word already used')
        if played_words.gamer == user.pk:
            user_words = played_words
    if user_words is not None:
        user_words.words.append(word)
    else:
        game.played_words.append(PlayedWords(gamer=user.pk, words=[word]))
    prepared_letters = []
    for letter in letters:
        db_letter = get_letter_by_id(game, letter)
        db_letter.gamer = user.pk
        prepared_letters.append(db_letter.letter_id)
    game.save()
    game.change_current_player()
    return prepared_letters


def send_event(event_type, event_data, session_id, user=None):
    to_send = {
        'event': event_type,
        'data': event_data,
        'session_id': session_id,
        'user': user
        }
    urllib2.urlopen(settings.ASYNC_BACKEND_URL, urllib.urlencode(to_send))
