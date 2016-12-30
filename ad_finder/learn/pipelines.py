from sklearn.feature_extraction.text import (
    CountVectorizer,
    TfidfTransformer,
)
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


def baseline_pipeline():
    return Pipeline(
        [
            ('vect', CountVectorizer()),
            # ('tfidf', TfidfTransformer()),
            ('clf', MultinomialNB()),
        ])


def svm_pipeline():
    return Pipeline(
        [
            ('vect', CountVectorizer()),
            # ('tfidf', TfidfTransformer()),
            ('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=5, random_state=42)),
        ]
    )


def get_pipeline(name):
    if name == 'baseline':
        return baseline_pipeline()
    if name == 'svm':
        return svm_pipeline()
    raise Exception('Unknown pipeline {}'.format(name))
