import random
import string
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


def get_letter_by_id(game, letter_id):
    for letter in game.letters:
        if letter.letter_id == letter_id:
            return letter.letter
    raise DoesNotExist('No such letter')
