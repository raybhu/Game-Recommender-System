import os
import json
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors


def findKSimilarCritic(userRowNumber, scoreMatrix, rowNames, metric='cosine', k=5):
    # find k similar users
    similarities = []
    indices = []
    model_knn = NearestNeighbors(metric=metric, algorithm='auto')
    model_knn.fit(scoreMatrix)
    distances, indices = model_knn.kneighbors(
        scoreMatrix.iloc[userRowNumber-1, :].values.reshape(1, -1), n_neighbors=k)
    similarities = 1-distances.flatten()
    print('{0} most similar users for User at {1} row:\n'.format(k-1, userRowNumber))
    for i in range(0, len(indices.flatten())):
        if indices.flatten()[i]+1 == userRowNumber:
            continue
        else:
            print('{0}: {1}, with similarity of {2}'.format(
                i, rowNames[indices.flatten()[i]], similarities.flatten()[i]))
    return similarities, indices


def predict_userbased(userRowNumber, gameColumnNumber, scoreMatrix, rowNames, columnNames):
    prediction = 0
    similarities, indices = findKSimilarCritic(
        userRowNumber, scoreMatrix, rowNames)
    # similar users based on cosine similarity
    mean_rating = scoreMatrix.loc[userRowNumber-1, :].mean()
    # to adjust for zero based indexing
    sum_wt = np.sum(similarities)-1
    product = 1
    wtd_sum = 0

    for i in range(0, len(indices.flatten())):
        if indices.flatten()[i]+1 == userRowNumber:
            continue
        else:
            ratings_diff = scoreMatrix.iloc[indices.flatten()[
                i], gameColumnNumber-1]-np.mean(scoreMatrix.iloc[indices.flatten()[i], :])
            product = ratings_diff * (similarities[i])
            wtd_sum = wtd_sum + product

    prediction = int(round(mean_rating + (wtd_sum/sum_wt)))
    print(
        '\nPredicted rating for user at {0} row -> game {1}: {2}'.format(userRowNumber, columnNames[gameColumnNumber-1], prediction))

    return prediction


# path
gameJSONFile = os.path.abspath(os.path.dirname(__file__)+'/games.json')
gameCleansedJSONFile = os.path.abspath(
    os.path.dirname(__file__)+'/games_cleansed.json')
criticScoreJSONFile = os.path.abspath(
    os.path.dirname(__file__)+'/critic_score.json')
with open(gameCleansedJSONFile, 'r') as f:
    gameList = json.load(f)
criticReviewsDict = {}
for gIndex, game in enumerate(gameList):
    for cReview in game['criticReviewsList']:
        if cReview['source'] not in criticReviewsDict.keys():
            criticReviewsDict[cReview['source']] = {}
            criticReviewsDict[cReview['source']
                              ][game['name']] = int(cReview['score'])
        else:
            criticReviewsDict[cReview['source']
                              ][game['name']] = int(cReview['score'])
# print(criticReviewsDict)
testDict = {'FIFA 18': 100, 'FIFA 17': 100,
            "FIFA 14": 100, 'Pro Evolution Soccer 2016': 0}
# testDict = {'God of War': '90'}
filteredCriticReviewsDict = {}
for cSourceName, cGameScoreDict in criticReviewsDict.items():
    sumScore = 0
    filteredScoreDict = {}
    for gName, gScore in cGameScoreDict.items():
        sumScore += int(gScore)
        if gName in testDict.keys():
            filteredScoreDict[gName] = gScore
    if filteredScoreDict:
        filteredCriticReviewsDict[cSourceName] = filteredScoreDict
        for key, value in testDict.items():
            if key not in filteredCriticReviewsDict[cSourceName].keys():
                filteredCriticReviewsDict[cSourceName][key] = round(
                    sumScore / len(cGameScoreDict))
                # filteredCriticReviewsDict[cSourceName][key] = 0
print(filteredCriticReviewsDict)
with open(criticScoreJSONFile, 'w') as f:
    f.write(json.dumps(filteredCriticReviewsDict))
    f.close()
filteredCriticReviewsDict['User'] = testDict
scoreMatrix = pd.DataFrame(filteredCriticReviewsDict).transpose()
columnNames = scoreMatrix.columns.values
rowNames = scoreMatrix.index.values
userRowNumber = len(scoreMatrix.index)
scoreMatrix = pd.DataFrame(scoreMatrix.values)
print(scoreMatrix, scoreMatrix.values, userRowNumber)
# findKSimilarCritic(userRowNumber, scoreMatrix, rowNames)
predict_userbased(userRowNumber, 4, scoreMatrix, rowNames, columnNames)


def getRecommenderList(favoriteGamesDict):

    return True
