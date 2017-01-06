import numpy as np
from sklearn.feature_extraction.text import (
    CountVectorizer,
    HashingVectorizer,
    TfidfTransformer,
)
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from is_ad.learn.marisa_vectorizer import MarisaCountVectorizer


def baseline_pipeline():
    return Pipeline(
        [
            ('vect', MarisaCountVectorizer(ngram_range=(1, 2),
                                           stop_words='english',
                                           min_df=1)),
            ('tfidf', TfidfTransformer(norm=None)),
            ('clf', MultinomialNB()),
        ])


def hashing_baseline_pipeline():
    return Pipeline(
        [

            ('vect', HashingVectorizer(ngram_range=(1, 2),
                                       # analyzer=lambda s: s.split(),
                                       non_negative=True,
                                       # n_features=(2**20),
                                       norm='l2',
                                       stop_words='english',
                                       dtype=np.int64)),
            ('tfidf', TfidfTransformer()),
            ('clf', MultinomialNB()),
        ])


def svm_pipeline():
    return Pipeline(
        [
            ('vect', MarisaCountVectorizer(ngram_range=(1, 2))),
            ('tfidf', TfidfTransformer(norm=None)),
            ('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-2, n_iter=10, random_state=666)),
        ]
    )

_pipeline_dict = {
    'baseline': baseline_pipeline(),
    'svm': svm_pipeline(),
    'hashing_baseline': hashing_baseline_pipeline()
}


def get_pipeline(name):
    if not name in _pipeline_dict:
        raise ValueError('Unknown pipeline {}, available pipelines {}: '.format(name, _pipeline_dict.keys()))
    return _pipeline_dict[name]