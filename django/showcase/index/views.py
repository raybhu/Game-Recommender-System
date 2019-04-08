import sys
import os
import json
import platform
from django.shortcuts import render
import recommender_system.contentBased as cb

# Create your views here.


def index(request):
    """
    View function for home page of site.
    """

    gameJSONFile = os.path.abspath(
        os.curdir)+'/django/showcase/recommender_system/games.json'
    gameCleansedJSONFile = os.path.abspath(
        os.curdir)+'/django/showcase/recommender_system/games_cleansed.json'
    if request.method == 'GET':
        with open(gameCleansedJSONFile, 'r') as f:
            gameList = json.load(f)
    elif request.method == 'POST':
        if 'clear' in request.POST:
            print('1')
            request.session['favoriteGames'] = []
            with open(gameCleansedJSONFile, 'r') as f:
                gameList = json.load(f)
        elif 'name' in request.POST:
            gameName = request.POST['name']
            if not 'favoriteGames' in request.session or not request.session['favoriteGames']:
                tmpList = [gameName]
                request.session['favoriteGames'] = tmpList
            else:
                tmpList = request.session['favoriteGames']
                if gameName not in tmpList:
                    tmpList.append(gameName)
                    request.session['favoriteGames'] = tmpList
            gameList = cb.getRecommenderList(request.session['favoriteGames'])
            for x in gameList:
                print(x['name'])
            print(request.session['favoriteGames'])
        else:
            with open(gameCleansedJSONFile, 'r') as f:
                gameList = json.load(f)
    # Render the HTML template index.html with the data in the context variable

    return render(
        request,
        'index.html',
        context={'gameList': gameList}
    )
