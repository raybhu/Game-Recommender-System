# -*- coding: utf-8 -*-
from __future__ import print_function
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import metrics
from sklearn.cluster import KMeans
import numpy as np
# Load some categories from the training set
categories = ['alt.atheism', 'talk.religion.misc', 'comp.graphics', 'sci.space']
dataset = fetch_20newsgroups(subset='all', categories=categories)
labels = dataset.target
k = len(np.unique(labels))
vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, stop_words='english')
X = vectorizer.fit_transform(dataset.data)

# perform clustering
km = KMeans(n_clusters=k, max_iter=100, n_init=1)
km.fit_transform(X)

print('Clustering statistic:\n')
print('ARI: %0.3f' % metrics.adjusted_rand_score(labels, km.labels_))
print('Homogeneity: %0.3f' % metrics.homogeneity_score(labels, km.labels_))
print('Completeness: %0.3f' % metrics.completeness_score(labels, km.labels_))
print('V-measure: %0.3f\n' % metrics.v_measure_score(labels, km.labels_))

print('Top terms per cluster:')
order_centroids = km.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(k):
    print('Cluster %d:' % i)
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind])
    print()
