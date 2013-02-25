# coding: utf-8
from pymongo import MongoClient

connection = MongoClient()
db = connection.test_letters
words = db.english_words
words_file = open('2of4brif.txt', 'r')
i = 1
for word in words_file.readlines():
    words.insert({
        'word_id': i,
        'word': word.strip(),
        "_cls": "EnglishWords",  # just for mongoengine
        "_types": ["EnglishWords"],  # just for mongoengine
        })
    print (word.strip())
    i += 1
words_file.close()
connection.close()
print (words.count())
