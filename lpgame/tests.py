from django.test import TestCase
from django.contrib.auth.models import User
from base import MongoTestCase
from models import *


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class GameTest(MongoTestCase):
    def setUp(self):
        User.create_user(username='test_user', password='test')
        self.client.login()

    def letters_generator(self):
        pass
