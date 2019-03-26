from bs4 import BeautifulSoup
import platform
import requests
import json
import re
# path
if platform.system() == 'Darwin':
    gameJSONFile = './games.json'
elif platform.system() == 'Windows':
    gameJSONFile = 'games.json'
if platform.system() == 'Darwin':
    gameFilteredJSONFile = './games_filtered.json'
elif platform.system() == 'Windows':
    gameFilteredJSONFile = 'games_filtered.json'
# Crawler
topPS4GamesUrl = 'https://www.metacritic.com/browse/games/release-date/available/ps4/metascore'
headers = {'User-Agent': 'Mozilla/5.0'}
topPS4GamesHtml = requests.get(topPS4GamesUrl, headers=headers)
bs = BeautifulSoup(topPS4GamesHtml.text, 'lxml')
gameHtmlList = bs.find('ol', {'class': 'list_products list_product_condensed'}).find_all(
    'div', {'class': 'basic_stat product_title'})
gameList = []
for index, item in enumerate(gameHtmlList):
    print('The crawler is working on collecting %d game.' % (index+1))
    link = 'https://www.metacritic.com' + item.find('a')['href'] + '/'
    html = BeautifulSoup(requests.get(link, headers=headers).text, 'lxml')
    name = html.find('h1').text
    metaScore = html.find('span', {'itemprop': 'ratingValue'}).text
    regex = re.compile('metascore_w user*')
    userScore = html.find(
        'div', {'class': regex}).text
    if metaScore == 'tbd' or userScore == 'tbd':
        continue
    print(name, metaScore, userScore)
    criticReviewsListHtml = html.find_all(
        'li', class_="critic_review")
    userReviewsListHtml = html.find_all(
        'li', class_="user_review")
    criticReviewsList = []
    userReviewsList = []
    for cIndex, cReview in enumerate(criticReviewsListHtml):
        cSource = cReview.find('div', {'class': 'source'}).text
        cReviewBody = cReview.find('div', {'class': 'review_body'}).text
        cScore = cReview.find('div', {'class': 'metascore_w'}).text
        review = {"source": cSource, "review": cReviewBody, "score": cScore}
        criticReviewsList.append(review)
        print(cSource, cReviewBody, cScore)
    for uIndex, uReview in enumerate(userReviewsListHtml):
        uName = uReview.find('div', {'class': 'name'}).find('a').text
        expandedReview = uReview.find(
            'span', {'class': 'blurb blurb_expanded'})
        uReviewBody = expandedReview and expandedReview.text or uReview.find(
            'div', {'class': 'review_body'}).find('span').text
        uScore = uReview.find('div', {'class': 'metascore_w'}).text
        review = {"username": uName, "review": uReviewBody, "score": uScore}
        userReviewsList.append(review)
        print(uName, uReviewBody, uScore)
    game = {'name': name, 'metaScore': metaScore, 'userScore': userScore, 'URL': link,
            'criticReviews': criticReviewsList, 'userReviewsList': userReviewsList}
    gameList.append(game)

with open(gameJSONFile, 'w') as f:
    f.write(json.dumps(gameList))
    f.close()
