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

from ad_finder.util.web_util import get

app = Flask(__name__)
app.is_initialized = False

_version = 'v0.1'
_api_prefix = '/api/{}/categorize/'.format(_version)


def init(text_cf):
    """
    Initialize the web-app.

    Parameters
    ----------
    text_cf: `sklearn.base.BaseEstimator`
        Text classification model.
    """
    if app.is_initialized:
        raise ValueError('App is already initialized.')

    if not isinstance(text_cf, BaseEstimator):
        raise ValueError('classification model {}:{} is not a BaseEstimator'.format(text_cf, type(text_cf)))
    app.text_cf = text_cf
    app.is_initialized = True


def _predict(text):
    """Categorise text.
    0 : not an ad.
    1: is an ad.

    Parameters
    ----------
    text: `str`
        The text to be categorised.

    Returns
    -------
    flask.Response
        To send to client.
    """
    print('text')
    print(text)

    classification = app.text_cf.predict([text])
    return jsonify({'category': classification[0]})


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


@app.route(_api_prefix + 'text', methods=['PUT'])
def classify_text():
    _ensure_initialized()
    text = request.data
    if text is None:
        return 'Missing request data : no text to classify', 400
    return _predict(text)


@app.route(_api_prefix + 'url')
def classify_url():
    _ensure_initialized()
    url = request.args.get('url', None)
    if url is None:
        return 'Missing query parameter: url', 400
    page = get(url)
    return _predict(page)
