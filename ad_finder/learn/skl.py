import logging
import numpy as np
from sklearn import metrics
from ad_finder.learn.pipelines import get_pipeline
from ad_finder.learn.pipeline_input import PipelineInput


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
    test_doc_categories = np.array(pipeline_input.test_doc_categories())

    mean = np.mean(predicted_cats == test_doc_categories)
    logging.info('Average success rate {:.3f}.'.format(mean))

    report = metrics.classification_report(predicted_cats,
                                           test_doc_categories,
                                           labels=['not ad', 'is ad'])
    print(report)
