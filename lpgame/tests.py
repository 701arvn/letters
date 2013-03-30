from django.contrib.auth.models import User
from base import MongoTestCase
from models import *


class GameTest(MongoTestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test')
        self.user2 = User.objects.create_user(username='test_user2', password='test')
        # self.client.login()

    def test_are_25_letters(self):
        letters = generate_letters()
        self.assertEqual(len(letters), 25)

    def test_is_game_generated(self):
        session_id = '1234567'
        generate_game(self.user, session_id)
        game = Game.objects.get(session_id=session_id)
        self.assertIn(self.user.pk, game.gamers)
        self.assertEqual(len(game.letters), 25)

    def add_word_to_db(self):
        session_id = '1234567'
        game = generate_game(self.user, session_id)
        game.letters = game.letters[:21]
        self.assertEqual(len(game.letters), 21)
        word_letters = [
            Letter(letter_id=22, letter='w'),
            Letter(letter_id=23, letter='o'),
            Letter(letter_id=24, letter='r'),
            Letter(letter_id=25, letter='d'),
        ]
        game.letters += word_letters
        self.assertEqual(len(game.letters), 25)
        return game, word_letters

    def test_on_user_turn_first_turn(self):
        word = 'word'
        game, word_letters = self.add_word_to_db()
        on_user_turn(game, word, [l.letter_id for l in word_letters], self.user)
        self.assertIn(word, game.played_words[0].words)
        for word_letter in word_letters:
            self.assertIn(word_letter, game.letters)
            self.assertEqual(word_letter.gamer, self.user.pk)
        # tests that you cant use same word twice
        self.assertRaises(
            Exception,
            on_user_turn,
            game, word, [l.letter_id for l in word_letters], self.user
        )
        # tests that other user also cant use this word
        self.assertRaises(
            Exception,
            on_user_turn,
            game, word, [l.letter_id for l in word_letters], self.user2
        )

    def test_check_only_two_users_in_game(self):
        #TODO if possible
        pass
