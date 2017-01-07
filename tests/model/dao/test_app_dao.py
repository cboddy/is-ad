from is_ad.model.dao.common import *
from is_ad.model.document import Document
from is_ad.model.model import Model

from is_ad.model.dao.app_dao import get_document
from is_ad.model.dao.app_dao import add_document
from uuid import uuid4

configure()


def _random():
    return str(uuid4())


def test_get_document():
    model_name = _random()
    doc_url = _random()
    doc_text = _random()
    doc_category = 1

    with session_scope() as session:
        model = Model(name=model_name)
        session.add(model)

    with session_scope() as session:
        document = Document(text=doc_text, category=doc_category, url=doc_url, model_id=model.id)
        session.add(document)

    doc = get_document(doc_url, model_name)
    assert doc is not None
    assert doc.url == doc_url
    assert doc.text == doc_text
    assert doc.category == doc_category

    missing_doc = get_document('missing', model_name)
    assert missing_doc is None


def test_add_document():
    model_name = _random()
    doc_url = _random()
    doc_text = _random()
    doc_category = 1

    with session_scope() as session:
        model = Model(name=model_name)
        session.add(model)

    add_document(doc_text, doc_category, doc_url, model_name)

    # document with url
    doc = get_document(doc_url, model_name)
    assert doc is not None

    # docuemnt without url
    add_document(doc_text, doc_category, None, model_name)
    doc = get_document(doc_url, model_name)
    assert doc is not None
    assert doc.url == doc_url
