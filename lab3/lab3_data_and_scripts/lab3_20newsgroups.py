# -*- coding: utf-8 -*-
from sklearn.datasets import fetch_20newsgroups

# The reference of the data set 20 Newsgroups can be found here:
# http://qwone.com/~jason/20Newsgroups/
# The usage of fetch_20newsgroups can be found here:
# http://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch_20newsgroups.html#sklearn.datasets.fetch_20newsgroups
newsgroups_data = fetch_20newsgroups(subset='all')
# list out all the categories name in the dataset
print('newsgroups_data.target_names:')
print(newsgroups_data.target_names)
print('')

print('Size of newsgroups_data.data: %d' % len(newsgroups_data.data))
for i in range(3):
    print('Doc Number %d' % i)
    print('Target Index: %d' % newsgroups_data.target[i])
    print('Doc Type: %s' % newsgroups_data.target_names[newsgroups_data.target[i]])
    print(newsgroups_data.data[i])
    print('')
