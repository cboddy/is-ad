import logging
import re
import time
import zipfile
from functools import wraps

from ad_finder.util.zip_util import zip_iter
from bs4 import BeautifulSoup

NON_VISIBLE_LABELS = ['style', 'script', '[document]', 'head', 'title']
LOG = logging.getLogger(__name__)


def log_time(func):
    """Utility decorator for profiling method calls."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        msg = ' '.join([func.__name__, '(',str(args), str(kwargs), ')',
                        'took', str(duration), 'seconds.'])
        # LOG.info(msg)
        print(msg)
        return result
    return wrapper


@log_time
def parse_zip(zip_path, text_consumer):
    for name, z_open in zip_iter(zip_path):
        text = parse_texts(z_open)
        text_consumer(name, text)


def parse_texts(iterator):
    """
    Filter the visible text from an html doc.

    Parameters
    ----------
    iterator: `str`
        The html doc.

    Returns
    -------
    list[str]
    Visible text filtered from the html doc.
    """
    soup = BeautifulSoup(iterator, 'lxml')
    text_elements = soup.findAll(text=True)
    visible_texts = [elem for elem in text_elements if _is_visible(elem)]
    return visible_texts


def _is_visible(element):
    """
    Does the page element hold visible text.

    Parameters
    ----------
    element: `BeautfulSoup.PageElement`

    Returns
    -------
    bool
        True iff element holds visible text
    """
    as_str = unicode(element)
    if element.parent.name in NON_VISIBLE_LABELS:
        return False
    if re.match('<!--.*-->', as_str):
        return False
    if not len(''.join(as_str.split())):
        return False
    return True


def unzip_and_extract_text(zip_path, output_path):
    logging.info('Running  text extraction for {} -> {}'.format(zip_path, output_path))
    with zipfile.ZipFile(output_path, 'w', allowZip64=True) as z_out:
            for name, iterator in zip_iter(zip_path):
                LOG.debug('Writing {}'.format(name))
                try:
                    texts = parse_texts(iterator)
                    text = ''.join(texts).encode('utf-8')
                except Exception:
                    logging.error('Problem extracting text from {}/{}'.format(zip_path, name), exc_info=True)
                    continue

                z_out.writestr(name, text)

