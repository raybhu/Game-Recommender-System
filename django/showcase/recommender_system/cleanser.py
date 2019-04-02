import nltk
import os
import json
import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
import langid


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


# cleanser
with open(gameJSONFile, 'r') as f:
    gameList = json.load(f)

for index, game in enumerate(gameList):
    print('The Cleanser is working on %d game.' % (index+1))
    tmpCriticReviewsList = []
    for cIndex, criticReview in enumerate(game['criticReviewsList']):
        if langid.classify(criticReview['review'])[0] == "en":
            review = stopword_filtered(criticReview['review'].split())
            review = ' '.join(review)
            review = re.sub(
                '[;:.,!?\-/+^\'’_$%*()`~\"@#&={}\[\]|\\\\<>]', '', review)
            criticReview['review'] = review
            tmpCriticReviewsList.append(criticReview)
    gameList[index]['criticReviewsList'] = tmpCriticReviewsList
    tmpUserReviewsList = []

    for uIndex, userReview in enumerate(game['userReviewsList']):
        if langid.classify(userReview['review'])[0] == "en":
            review = stopword_filtered(userReview['review'].split())
            review = ' '.join(review)
            review = re.sub(
                '[;:.,!?\-/+^\'’_$%*()`~\"@#&={}\[\]|\\\\<>]', '', review)
            userReview['review'] = review
            tmpUserReviewsList.append(userReview)
    gameList[index]['userReviewsList'] = tmpUserReviewsList


with open(gameCleansedJSONFile, 'w') as f:
    f.write(json.dumps(gameList))
    f.close()
