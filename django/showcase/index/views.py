import sys
import os
import json
import platform
from django.shortcuts import render
import recommender_system.contentBased as cb
import recommender_system.collaborativeFiltering as cf

# Create your views here.


def index(request):
    """
    View function for home page of site.
    """
    gameCleansedJSONFile = os.path.abspath(
        os.curdir)+'/django/showcase/recommender_system/games_cleansed.json'
    gameList = []
    rsMethod = 1
    if request.method == 'GET':
        with open(gameCleansedJSONFile, 'r') as f:
            gameList = json.load(f)
        rsMethod = 1
    elif request.method == 'POST':
        if 'clear' in request.POST:

            request.session['favoriteGames'] = []
            request.session['scoredGames'] = []
            rsMethod = int(request.POST['currentMethod'])

            with open(gameCleansedJSONFile, 'r') as f:
                gameList = json.load(f)

        elif 'name' in request.POST:
            rs = int(request.POST['method'])
            print(rs)
            if rs == 1:
                gameName = request.POST['name']
                if not 'favoriteGames' in request.session or not request.session['favoriteGames']:
                    tmpList = [gameName]
                    request.session['favoriteGames'] = tmpList
                else:
                    tmpList = request.session['favoriteGames']
                    if gameName not in tmpList:
                        tmpList.append(gameName)
                        request.session['favoriteGames'] = tmpList
                gameList = cb.getRecommenderList(
                    request.session['favoriteGames'])
                for x in gameList:
                    print(x['name'])
                rsMethod = 1
                print(request.session['favoriteGames'])
            elif rs == 2:
                gameName = request.POST['name']
                gameScore = int(request.POST['score'])
                if not 'scoredGames' in request.session or not request.session['scoredGames']:
                    tmpDict = {gameName: gameScore}
                    request.session['scoredGames'] = tmpDict
                else:
                    tmpDict = request.session['scoredGames']
                    if gameName not in tmpDict.keys():
                        tmpDict[gameName] = gameScore
                        request.session['scoredGames'] = tmpDict
                gameList = cf.getRecommenderDict(
                    request.session['scoredGames'])
                for game in gameList:
                    print(game['name']+str(game['predictedScore']))
                rsMethod = 2
                print(request.session['scoredGames'])
        elif 'method' in request.POST:
            if request.POST['method'] == 'Content-Based':
                request.session['favoriteGames'] = []
                with open(gameCleansedJSONFile, 'r') as f:
                    gameList = json.load(f)
                rsMethod = 1
            elif request.POST['method'] == 'Collaborative-Filtering':
                request.session['scoredGames'] = []
                with open(gameCleansedJSONFile, 'r') as f:
                    gameList = json.load(f)
                rsMethod = 2

        else:
            with open(gameCleansedJSONFile, 'r') as f:
                gameList = json.load(f)
    # Render the HTML template index.html with the data in the context variable

    return render(
        request,
        'index.html',
        context={'gameList': gameList, 'rsMethod': rsMethod}
    )
