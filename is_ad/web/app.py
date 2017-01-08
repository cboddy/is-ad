import re
import os.path
from sklearn.base import BaseEstimator
from flask import (
    Flask,
    request,
    session,
    redirect,
    url_for,
    escape,
    Session,
    make_response,
    jsonify,
    send_from_directory,
)

from is_ad.util.web_util import get
from is_ad.parse.html import parse_text
from is_ad.model.dao.common import (
    get_engine,
    configure
)
from is_ad.model.dao.app_dao import (
    add_document,
    add_view,
    get_document,
    ensure_model_present
)

app = Flask(__name__)
app.is_initialized = False

_version = 'v0.1'
_api_prefix = '/api/{}/categorize/'.format(_version)

_url_regex = re.compile(
        r'^(http)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def init(text_cf,
         name,
         db_url):
    """
    Initialize the web-app.

    Parameters
    ----------
    text_cf: `sklearn.base.BaseEstimator`
        Text classification model.
    name: `str`
        Classification model name
    db_url: `str`
        Url to DB resource.
    """
    if app.is_initialized:
        raise ValueError('App is already initialized.')
    # setup DB engine
    db_engine = get_engine(db_url)
    configure(db_engine)
    # setup model name and ensure present in DB
    ensure_model_present(name)
    app.name = name
    # setup text classifier
    if not isinstance(text_cf, BaseEstimator):
        raise ValueError('classification model {}:{} is not a BaseEstimator'.format(text_cf, type(text_cf)))
    app.text_cf = text_cf
    app.is_initialized = True


def _is_valid_url(url):
    """Is url a valid URL that starts http(s)://"""
    return _url_regex.match(url) is not None


def _get_response(category):
    """Build text categorisation response.

    Parameters
    ----------
    category: int
        0 : not an ad.
        1: is an ad.

    Returns
    -------
    flask.Response
        To send to client.
    """
    return jsonify({'category': category})


def _ensure_initialized():
    """Ensure app is initialized."""
    if not app.is_initialized:
        raise ValueError('App is not initialized.')


@app.route('/<path:filename>')
def static_content(filename):
    return send_from_directory('public', filename)


@app.route('/')
def redirect_to_index():
    return static_content('index.html')


@app.route(_api_prefix + 'text', methods=['POST'])
def classify_text():
    _ensure_initialized()
    text = request.data
    if text is None:
        return 'Missing request data : no text to classify', 400
    category = app.text_cf.predict([text])[0]
    return _get_response(category)


@app.route(_api_prefix + 'url', methods=['GET'])
def classify_url():
    _ensure_initialized()
    url = request.args.get('url', None)
    if url is None:
        return 'Missing query parameter: url', 400
    if not _is_valid_url(url):
        return 'Specified url "{}" is not valid or does not start http(s)://'.format(url), 400

    doc = get_document(url, app.name)
    if doc is None:
        page = get(url)
        text = parse_text(page)
        category = app.text_cf.predict([text])[0]
        doc = add_document(text, category, url, app.name)

    add_view(doc.id)
    return _get_response(doc.category)
