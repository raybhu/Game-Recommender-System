# -*- coding: utf-8 -*-
import re
from nltk.corpus import stopwords
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures


def stopword_filtered(words):
    filtered_list = []
    stop_set = set(stopwords.words('english'))
    # print(stop_set)
    for w in words:
        if w not in stop_set:
            filtered_list.append(w)
    return filtered_list


def bigram_word_feats(words, score_fn=BigramAssocMeasures.chi_sq, n=50):
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    return bigrams


if __name__ == '__main__':
    with open('n_gram_input_text.txt', 'r') as f:
        content = ''
        for line in f.readlines():
            content += line
        content = content.strip()
        content = re.sub('[^A-Za-z\s]', ' ', content)
        content = content.lower()
        word_list = content.split()
        filtered_list = stopword_filtered(word_list)
        bigram = bigram_word_feats(filtered_list)
        print(bigram)
