import nltk
import os
import json
import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
# path
gameJSONFile = os.path.abspath(os.path.dirname(__file__)+'/games.json')
gameCleansedJSONFile = os.path.abspath(
    os.path.dirname(__file__)+'/games_cleansed.json')
# stopword
# nltk.download('stopwords')

ENGLISH_STOP_WORDS = set(stopwords.words(
    'english')+['\n']
).union(set(ENGLISH_STOP_WORDS))
# print(ENGLISH_STOP_WORDS)


def stopword_filtered(words):
    filtered_list = []
    for w in words:
        w = w.lower()
        if w not in ENGLISH_STOP_WORDS:
            filtered_list.append(w)
    return filtered_list


# judge english


def judge_pure_english(keyword):
    return all(ord(c) < 128 for c in keyword)


# cleanser
with open(gameJSONFile, 'r') as f:
    gameList = json.load(f)

for index, game in enumerate(gameList):
    print('The Cleanser is working on %d game.' % (index+1))
    for cIndex, criticReview in enumerate(game['criticReviewsList']):
        # print(criticReview)
        review = stopword_filtered(criticReview['review'].split())
        review = ' '.join(review)
        review = re.sub(
            '[;:.,!?\-/+^\'’_$%*()`~\"@#&={}\[\]|\\\\<>]', '', review)
        if judge_pure_english(review):
            gameList[index]['criticReviewsList'][cIndex]['review'] = review
        else:
            gameList[index]['criticReviewsList'].pop(cIndex)
    print(gameList[index]['criticReviewsList'])
    for uIndex, userReview in enumerate(game['userReviewsList']):
        review = stopword_filtered(userReview['review'].split())
        review = ' '.join(review)
        review = re.sub(
            '[;:.,!?\-/+^\'’_$%*()`~\"@#&={}\[\]|\\\\<>]', '', review)
        if judge_pure_english(review):
            gameList[index]['userReviewsList'][uIndex]['review'] = review

        else:
            gameList[index]['userReviewsList'].pop(uIndex)
    print(gameList[index]['userReviewsList'])

with open(gameCleansedJSONFile, 'w') as f:
    f.write(json.dumps(gameList))
    f.close()
