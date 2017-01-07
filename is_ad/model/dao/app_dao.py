import logging
import datetime
from sqlalchemy.orm import defer
from is_ad.model.dao.common import session_scope
from is_ad.model.document import Document
from is_ad.model.model import Model
from is_ad.model.view import View

LOG = logging.getLogger(__name__)


def get_document(url, model_name, with_session=None):
    """
    Get the document with specified url and model_name.

    Parameters
    ----------
    url: `str`
    model_name: `str`
    with_session: `sqlalchemy.Session`
        USed to query DB. A new session is created when None.

    Returns
    -------
    Document or None
        The document with the url and model_name or None if it doesn't exist.
    """
    with session_scope(with_session) as session:
        return session.query(Document) \
            .filter(Document.url == url) \
            .join(Model, Model.id == Document.model_id) \
            .filter(Model.name == model_name) \
            .first()



def add_view(doc_id,
             timestamp=None,
             with_session=None):
    """

    Parameters
    ----------
    doc_id: `int`
    timestamp: datetime.datetime
        Defaults to `now` when None.
    with_session: `sqlalchemy.Session`
        Defaults to a new session when None.

    Returns
    -------

    """
    if timestamp is None:
        timestamp == datetime.datetime()

    with session_scope(with_session) as session:
        session.add(View(doc_id,
                         timestamp))


def add_model(name):
    with session_scope() as session:
        session.add(Model(name=name))


def add_document(text,
                 category,
                 url,
                 model_name):
    with session_scope() as session:
        model = session.query(Model) \
            .filter_by(name=model_name) \
            .first()
        if model is None:
            raise ValueError('No model with name {}.'.format(model_name))

        document = Document(text=text,
                            category=category,
                            url=url,
                            model_id=model.id)
        session.add(document)
        return document
