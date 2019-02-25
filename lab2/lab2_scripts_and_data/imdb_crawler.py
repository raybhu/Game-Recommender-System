# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 23:00:18 2019
@author: csleili
"""

import requests
from bs4 import BeautifulSoup

movie = 'http://www.imdb.com/title/tt2527336/'
html = requests.get(movie)  # connect to the server

bs = BeautifulSoup(html.text, 'lxml')  # manage tags in HTML document

# crawl movie name
name = bs.find('h1')  # locate
movie_name = name.get_text().strip()  # extract text
print(movie_name)

# crawl movie description
desc = bs.find('div', {'class': 'summary_text'})
movie_desc = desc.get_text().strip()
print(movie_desc)

# crawl the poster
poster = bs.find('div', {'class': 'poster'})
img = poster.find('img')
img_link = img['src']  # access the value of an attribute of a tag
image = requests.get(img_link)
with open('star_war_poster.jpg', 'wb') as f:
    f.write(image.content)  # writing the picture

# extract links to other movies from the 'People who liked this also liked...' module
recommended_movies = bs.find('div', {'class': 'rec_page'})
movie_list = recommended_movies.find_all('div', {'class': 'rec_item'})
for ml in movie_list:
    movie_id = ml['data-tconst']
    movie_link = 'http://www.imdb.com/title/' + movie_id + '/'
    print(movie_link)
