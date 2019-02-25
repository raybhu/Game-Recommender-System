# -*- coding: utf-8 -*-
# clustering dataset
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt

x = np.array([2.0, 2.3, 2.1, 3.2, 3.8, 3.1, 3, 2, 0.5, 2.5, 0.5, 1, 3.4, 2.5, 4, 0.1, 0.8, 3.2, 2, 0.5])
y = np.array([1.3, 2.2, 0.6, 1.5, 3.5, 2.5, 4, 2, 4.1, 4.4, 1.3, 2, 0.8, 3.1, 3, 1.2, 3.3, 2.4, 3, 1.0])

# plot a scatter plot for the data set
plt.scatter(x, y)
plt.title('Data set Distribution') 
plt.xlim([0, 5])
plt.ylim([0, 5])
plt.show()

# prepare for kMeans algorithm
X = np.array(list(zip(x, y)))
K = 3
# initiallize centroids
centroids = np.array([(0, 0), (3, 3), (6, 6)])
# prepare for plotting
colors = ['b', 'g', 'c']
markers = ['o', 'v', 's']
for i in range(1, 4):
    print('========For iteration %i========' % i)
    print('Centroids before applying kmeans:')
    print(centroids)
    # force the iteration to 1 by setting max_iter = 1 so that we can get the result for each iteration
    kmeans_model = KMeans(n_clusters=K, init=centroids, max_iter=1).fit(X)
    # update centroids after each iteration
    centroids = np.array(kmeans_model.cluster_centers_)
    print('Centroids after applying kemans:')
    print(centroids)
    plt.plot()
    plt.title('k means distribution in iteration %i' % i)
    for i, l in enumerate(kmeans_model.labels_):
        plt.plot(x[i], y[i], color=colors[l], marker=markers[l])
    plt.xlim([0, 5])
    plt.ylim([0, 5])
    plt.scatter(centroids[:, 0], centroids[:, 1], marker='x', color='r')
    plt.show()
