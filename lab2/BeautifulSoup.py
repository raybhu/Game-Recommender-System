import requests
from bs4 import BeautifulSoup
movie = 'http://www.imdb.com/title/tt2527336/'
html = requests.get(movie)
bs = BeautifulSoup(html.text, 'lxml')
desc = bs.find('div', {'class': 'summary_text'})
print(desc.get_text().strip())
poster = bs.find('div', {'class': 'poster'})
img = poster.find('img')
img_link = img['src']
image = requests.get(img_link)
with open('star_war_poster.jpg', 'wb') as f:
    f.write(image.content)
print(img_link)

recommended_movies = bs.find('div', {'class': 'rec_page'})
movie_list = recommended_movies.find_all('div', {'class': 'rec_item'})
for ml in movie_list:
    movie_id = ml['data-tconst']
    movie_link = 'http://www.imdb.com/title/'+movie_id + '/'
    print(movie_link)
