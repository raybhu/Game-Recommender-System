from __future__ import print_function
import os
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


def getRecommenderList(favoriteGamesList):
    # path
    gameJSONFile = os.path.abspath(os.path.dirname(__file__)+'/games.json')
    gameCleansedJSONFile = os.path.abspath(
        os.path.dirname(__file__)+'/games_cleansed.json')
    # tranformer
    with open(gameCleansedJSONFile, 'r') as f:
        gameList = json.load(f)
    # print(gameList)

    for index, game in enumerate(gameList):
        reviewSum = ''
        for review in game['criticReviewsList']:
            if review['score'] and int(review['score']) >= 88:
                reviewSum = reviewSum+review['review']
        # valuableCriticReviewList.append(reviewSum)
        gameList[index]['reviewSum'] = reviewSum

    # gamesUserLikedIndex = [10, 20, 30, 40, 50]
    gamesUserLikedIndex = []
    # for index, game in enumerate(gameList):
    #     if 'FIFA' in game['name'] and len(gamesUserLikedIndex) is not 3:
    #         gamesUserLikedIndex.append(index)

    for index, game in enumerate(gameList):
        if game['name'] in favoriteGamesList:
            gamesUserLikedIndex.append(index)

    valuableCriticReviewList = []
    for index in gamesUserLikedIndex:
        valuableCriticReviewList.append(gameList[index]['reviewSum'])

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
                gameList[gIndex]['similaritySum'] = sumResult
                # print(sumResult)
                similarityResultDict[gameList[gIndex]['name']] = sumResult
        else:
            gameList[gIndex]['similaritySum'] = 0
    for gIndex in gamesUserLikedIndex:
        print(gameList[gIndex]['name'])
    print(sorted(similarityResultDict.items(), key=lambda x: x[1]))
    gameList = sorted(gameList, key=lambda e: e['similaritySum'], reverse=True)
    return gameList
# game_index = list(range(1, len(gamesUserLikedIndex)+1))
# df = pd.DataFrame(X.todense(), index=game_index,
#                   columns=vectorizer.get_feature_names())
# print(df)
# writer = ExcelWriter('tf-idf.xlsx')
# df.to_excel(writer, 'tf-idf')
# writer.save()


getRecommenderList(['Grand Theft Auto V'])
