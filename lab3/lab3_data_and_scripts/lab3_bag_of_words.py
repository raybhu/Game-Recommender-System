# -*- coding: utf-8 -*-

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer

categories = ['alt.atheism', 'comp.graphics', 'sci.med', 'soc.religion.christian']
twenty_train = fetch_20newsgroups(subset='train', categories=categories)
count_vect = CountVectorizer()
bow_train_counts = count_vect.fit_transform(twenty_train.data)

print('Number of documents in twenty_train.data:')
print(len(twenty_train.data))
print('Number of extracted features:')
print(len(count_vect.get_feature_names()))
print('Size of bag-of-words:')
print(bow_train_counts.shape)

print('Bag of words: [(doc_id, features_id): Occurrence]')
print(bow_train_counts)
# print(bow_train_counts[0])
# print(bow_train_counts[0, 0])
# print(bow_train_counts[0, 230])
print(count_vect.get_feature_names())
