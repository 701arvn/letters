from django.test import TestCase
from django.contrib.auth.models import User
from base import MongoTestCase
from models import *


class GameTest(MongoTestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test')
        self.client.login()

    def test_are_25_letters(self):
        letters = generate_letters()
        self.assertEquals(len(letters), 25)

    def test_is_game_generated(self):
        session_id = '1234567'
        generate_game(self.user, session_id)
        game = Game.objects.get(session_id=session_id)
        self.assertIn(self.user.pk, game.gamers)
        self.assertEquals(len(game.letters), 25)

