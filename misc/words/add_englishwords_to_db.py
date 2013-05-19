# coding: utf-8
import os
from pymongo import MongoClient

connection = MongoClient(host=os.environ.get('MONGOHQ_URL', 'localhost'))
db = connection.letters
words = db.english_words
words_filename = os.path.join(os.path.dirname(__file__), '2of4brif.txt')
words_file = open(words_filename, 'r')
i = 1
try:
    for word in words_file.readlines():
        words.insert({
            'word_id': i,
            'word': word.strip(),
            "_cls": "EnglishWords",  # just for mongoengine
            "_types": ["EnglishWords"],  # just for mongoengine
            })
        print (word.strip())
        i += 1
finally:
    words_file.close()
    connection.close()
print (words.count())
