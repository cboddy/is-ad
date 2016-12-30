from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.datasets.base import Bunch
from sklearn.pipeline import Pipeline
import numpy as np


def gen_docs():
    docs = [
        'something something, dark side',
        'blah blah something blah',
        'is this enough now?'
    ]
    for doc in docs:
         yield doc
    #return docs


def get_bunch():
    target = np.zeros((3,), dtype=np.int64)
    target[1] = 1
    return Bunch(data=gen_docs(), target=target)


def run():

    docs = gen_docs()
    all_docs = list(gen_docs())

    target = np.zeros((3,), dtype=np.int64)
    target[1] = 1
    target[2] = 2
    print(docs, target)

    pipeline = Pipeline([('vect', CountVectorizer()),
                         ('tfidf', TfidfTransformer()),
                         ('clf', MultinomialNB()),
                         ])


    text_clf = pipeline.fit(docs, target)

    predicted = text_clf.predict([all_docs[1]])
    print(predicted)
    print('Done.')


class CMTest(object):
    def __init__(self, x):
        self.x = x

    def __enter__(self):
        print(self.__class__, '{} enter'.format(self.x))

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(self.__class__, '{} exit'.format(self.x))


def test_cm():

    print('starting')

    with CMTest('outer '):
        for i in xrange(10):
            with CMTest('inner'+str(i)):
                yield i

    print('done')

for i in test_cm():
    pass


# run()


