from __future__ import print_function
import platform
import json
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import metrics
from sklearn.metrics import pairwise_distances
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from pandas import ExcelWriter
import numpy as np
# path
if platform.system() == 'Darwin':
    gameJSONFile = './games.json'
elif platform.system() == 'Windows':
    gameJSONFile = 'games.json'
if platform.system() == 'Darwin':
    gameCleansedJSONFile = './games_cleansed.json'
elif platform.system() == 'Windows':
    gameCleansedJSONFile = 'games_cleansed.json'
# tranformer
with open(gameCleansedJSONFile, 'r') as f:
    gameList = json.load(f)
# print(gameList)


for index, game in enumerate(gameList):
    reviewSum = ''
    for review in game['criticReviewsList']:
        if review['score'] and int(review['score']) >= 90:
            reviewSum = reviewSum+review['review']
    # valuableCriticReviewList.append(reviewSum)
    gameList[index]['reviewSum'] = reviewSum

gamesUserLikedIndex = [1, 3, 5, 7, 9]
valuableCriticReviewList = []
for index in gamesUserLikedIndex:
    valuableCriticReviewList.append(gameList[index]['reviewSum'])
print(len(valuableCriticReviewList))

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(valuableCriticReviewList)
print(type(X), X.toarray(), X.shape, vectorizer.get_feature_names)
# print(X[:, 0:50].toarray())
similarityResultDict = {}
for gIndex, game in enumerate(gameList):
    if gIndex not in gamesUserLikedIndex:
        vectorizer_1 = TfidfVectorizer()
        reviewSum = gameList[gIndex]['reviewSum']
        if reviewSum:
            listTesta = list(valuableCriticReviewList)

            listTesta.insert(0, reviewSum)
            Y = vectorizer_1.fit_transform(listTesta)
            print(cosine_similarity(Y[0: 1], Y))
            sumResult = np.sum(cosine_similarity(Y[0: 1], Y))
            # print(sumResult)
            similarityResultDict[gameList[gIndex]['name']] = sumResult
print(sorted(similarityResultDict.items(), key=lambda x: x[1], reverse=True))


# game_index = list(range(1, len(gamesUserLikedIndex)+1))
# df = pd.DataFrame(X.todense(), index=game_index,
#                   columns=vectorizer.get_feature_names())
# print(df)
# writer = ExcelWriter('tf-idf.xlsx')
# df.to_excel(writer, 'tf-idf')
# writer.save()
# X = np.sum(X.toarray(), axis=0)

# X = np.true_divide(X, 5)
