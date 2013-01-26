from mongonaut.sites import MongoAdmin

from models import EnglishWords, Game

EnglishWords.mongoadmin = MongoAdmin()
Game.mongoadmin = MongoAdmin()