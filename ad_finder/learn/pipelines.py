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
            ('vect', CountVectorizer(ngram_range=(1,2))),
            # ('tfidf', TfidfTransformer(use_idf=False)),
            ('clf', MultinomialNB()),
        ])


def svm_pipeline():
    return Pipeline(
        [
            ('vect', CountVectorizer(ngram_range=(1,2))),
            # ('tfidf', TfidfTransformer(use_idf=False)),
            ('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=5, random_state=42)),
        ]
    )

_pipeline_dict = {
    'baseline': baseline_pipeline(),
    'svm': svm_pipeline()
}


def get_pipeline(name):
    if not name in _pipeline_dict:
        raise ValueError('Unknown pipeline {}, available pipelines {}: '.format(name, _pipeline_dict.keys()))
    return _pipeline_dict[name]