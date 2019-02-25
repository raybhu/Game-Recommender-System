# -*- coding: utf-8 -*-
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
import numpy as np

categories = ['alt.atheism', 'comp.graphics',
              'sci.med', 'soc.religion.christian']
twenty_train = fetch_20newsgroups(subset='train', categories=categories)

# tokenizing text with sk-learn
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(twenty_train.data)

# tf–idf can be computed as follows:
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
# print(type(X_train_tfidf))

# train classifier
clf = MultinomialNB().fit(X_train_tfidf, twenty_train.target)

# Prepare the testing data set
twenty_test = fetch_20newsgroups(subset='test', categories=categories)
new_doc = ['God is love', 'OpenGL on the GPU is fast', 'Atheism is the absence of belief in the existence of deities',
           'Computer graphics are pictures and films created using computers', 'The Ten Commandments']
# X_test_counts = count_vect.transform(twenty_test.data)
X_test_counts = count_vect.transform(new_doc)
X_test_tfidf = tfidf_transformer.transform(X_test_counts)

# use the trained classifier to predict results for testing data set
predicted = clf.predict(X_test_tfidf)

# for doc, category in zip(twenty_test.data, predicted):
for doc, category in zip(new_doc, predicted):
    print('Classified as: %s\n%s\n' %
          (twenty_train.target_names[category], doc))

print('Accuracy: %.3f\n' % np.mean(predicted == twenty_test.target))
# confusion martix
print('Confusion Martix:')
print(metrics.confusion_matrix(twenty_test.target, predicted))
print('\n\n')
# classifaction report: precision, recall, f1-score, support
print('Classification Report:')
print(metrics.classification_report(twenty_test.target,
                                    predicted, target_names=twenty_test.target_names))
