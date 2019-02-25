# -*- coding: utf-8 -*-
from wordcloud import WordCloud
import matplotlib.pyplot as plt

text = 'To introduce the fundamental concepts as well as practical applications of contemporary \
        Artificial Intelligence incorporating knowledge discovery and data mining social \
        network intelligence and intelligent agents and advanced Information Technology in the \
        context of Web empowered social computing systems environments and activities To \
        discuss the techniques and issues central to the development of social computing and Web \
        intelligence systems'

# For detailed usage of class WordCloud(), you can refer to the following link:
# https://amueller.github.io/word_cloud/generated/wordcloud.WordCloud.html#wordcloud.WordCloud
wordcloud = WordCloud().generate(text)
# Output the generated file to current folder
wordcloud.to_file('wordcloud.png')
# For detailed usage of class matplotlib.pyplot, you can refer to the following links
# Matplotlib: https://matplotlib.org/index.html
# matplotlib.pyplot.imshow: https://matplotlib.org/api/_as_gen/matplotlib.pyplot.imshow.html
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
