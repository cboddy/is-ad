import logging
import numpy as np
import gzip
import pickle
from sklearn import metrics
from sklearn.model_selection import GridSearchCV
from is_ad.learn.pipelines import get_pipeline
from is_ad.learn.pipeline_input import PipelineInput

LOG = logging.getLogger(__name__)


def run(pipeline_input,
        pipeline_name):
    """

    Parameters
    ----------
    pipeline_input: `PipelineInput`
    pipeline_name: `str`
    """
    pipeline = get_pipeline(pipeline_name)

    train_docs = pipeline_input.train_docs()
    train_doc_categories = pipeline_input.train_doc_categories()

    text_clf = pipeline.fit(train_docs,
                            train_doc_categories)

    predicted_cats = text_clf.predict(pipeline_input.test_docs())
    test_doc_categories = pipeline_input.test_doc_categories()

    mean = np.mean(predicted_cats == test_doc_categories)
    logging.info('Average success rate {:.3f}.'.format(mean))

    report = metrics.classification_report(predicted_cats,
                                           test_doc_categories)

    logging.info(report)
    return text_clf, report


def run_grid_optimization(pipeline_input,
                          pipeline_name):

    pipeline = get_pipeline(pipeline_name)

    parameters = {
        'vect__ngram_range': [(1, 1), (1, 2),],
        # 'tfidf__use_idf': (True, False),
        'clf__alpha': (1e-2, 1e-3),
    }


    gs_clf = GridSearchCV(pipeline,
                          parameters,
                          n_jobs=3)

    gs_clf = gs_clf.fit(list(pipeline_input.train_docs()),
                        pipeline_input.train_doc_categories())

    predicted_cats = gs_clf.predict(pipeline_input.test_docs())
    test_doc_categories = np.array(pipeline_input.test_doc_categories())

    mean = np.mean(predicted_cats == test_doc_categories)
    logging.info('Average success rate {:.3f}.'.format(mean))

    best_score = gs_clf.best_score_
    print('best-score', best_score)

    for param_name in sorted(parameters.keys()):
        print('best-score-param {} : {}'.format(param_name, gs_clf.best_params_[param_name]))

    report = metrics.classification_report(predicted_cats,
                                           test_doc_categories)
    print(report)


def read_model(text_cf_path):
    """
    De-serialize model from file.

    Parameters
    ----------
    text_cf_path: `str`
        Path to pickled


    Returns
    -------
    sklearn.pipeline.Pipeline
    """
    if text_cf_path.endswith('.gz'):
        with gzip.open(text_cf_path, 'rb') as f:
            return pickle.load(f)
    else:
        with open(text_cf_path, 'rb') as f:
            return pickle.load(f)
