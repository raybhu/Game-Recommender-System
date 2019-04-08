
import os
import json

gameCleansedJSONFile = os.path.abspath(
    os.path.dirname(__file__)+'/games_cleansed.json')
criticReviewsDictJSONFile = os.path.abspath(
    os.path.dirname(__file__)+'/critic_reviews.json')
with open(gameCleansedJSONFile, 'r', encoding='UTF-8') as f:
    gameList = json.load(f)
criticReviewsDict = {}
for game in gameList:
    for cReview in game['criticReviewsList']:
        if cReview['source'] not in criticReviewsDict.keys():
            criticReviewsDict[cReview['source']] = {}
            criticReviewsDict[cReview['source']
                              ][game['name']] = int(cReview['score'])
        else:
            criticReviewsDict[cReview['source']
                              ][game['name']] = int(cReview['score'])
with open(criticReviewsDictJSONFile, 'w') as f:
    f.write(json.dumps(criticReviewsDict))
    f.close()
