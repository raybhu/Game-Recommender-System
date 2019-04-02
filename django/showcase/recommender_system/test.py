from __future__ import print_function
import os
import json
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn import metrics
from sklearn.metrics import pairwise_distances
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from pandas import ExcelWriter
import numpy as np
# M is user-item ratings matrix where ratings are integers from 1-10
M = np.asarray([[3, 7, 4, 9, 9, 7],
                [7, 0, 5, 3, 8, 8],
                [7, 5, 5, 0, 8, 4],
                [5, 6, 8, 5, 9, 8],
                [5, 8, 8, 8, 10, 9],
                [7, 7, 0, 4, 7, 8]])
M = pd.DataFrame(M)

# declaring k,metric as global which can be changed by the user later
global k, metric
k = 4
metric = 'cosine'  # can be changed to 'correlation' for Pearson correlation similaries

# This function finds k similar users given the user_id and ratings matrix M
# Note that the similarities are same as obtained via using pairwise_distances


def findksimilarusers(user_id, ratings, metric=metric, k=k):
    similarities = []
    indices = []
    model_knn = NearestNeighbors(metric=metric, algorithm='brute')
    model_knn.fit(ratings)

    distances, indices = model_knn.kneighbors(ratings.iloc[user_id-1, :]
                                              .values.reshape(1, -1), n_neighbors=k)
    similarities = 1-distances.flatten()
    print('{0} most similar users for User {1}:\n'.format(k-1, user_id))
    for i in range(0, len(indices.flatten())):
        if indices.flatten()[i]+1 == user_id:
            continue

        else:
            print('{0}: User {1}, with similarity of {2}'.format(
                i, indices.flatten()[i]+1, similarities.flatten()[i]))

    return similarities, indices


findksimilarusers(3, M)


def predict_userbased(user_id, item_id, ratings, metric=metric, k=k):
    prediction = 0
    similarities, indices = findksimilarusers(user_id, ratings, metric, k)
    # similar users based on cosine similarity
    mean_rating = ratings.loc[user_id-1, :].mean()
    # to adjust for zero based indexing
    sum_wt = np.sum(similarities)-1
    product = 1
    wtd_sum = 0

    for i in range(0, len(indices.flatten())):
        if indices.flatten()[i]+1 == user_id:
            continue
        else:
            ratings_diff = ratings.iloc[indices.flatten()[i], item_id-1]
            -np.mean(ratings.iloc[indices.flatten()[i], :])
            product = ratings_diff * (similarities[i])
            wtd_sum = wtd_sum + product

    prediction = int(round(mean_rating + (wtd_sum/sum_wt)))
    print(
        '\nPredicted rating for user {0} -> item {1}: {2}'.format(user_id, item_id, prediction))

    return prediction


predict_userbased(3, 4, M)
