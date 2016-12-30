from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


def baseline_pipeline():
    return Pipeline(
        [
            ('vect', CountVectorizer()),
            ('tfidf', TfidfTransformer()),
            ('clf', MultinomialNB()),
        ])


def get_pipeline(name):
    if name == 'baseline':
        return baseline_pipeline()
    raise Exception('Unknown pipeline {}'.format(name))