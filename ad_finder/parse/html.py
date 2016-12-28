import re
from BeautifulSoup import BeautifulSoup
from ad_finder.parse.zip_util import zip_open_all

NON_VISIBLE_LABELS = ['style', 'script', '[document]', 'head', 'title']


def parse_zip(zip_path):
    for name, f_handle in zip_open_all(zip_path):
        pass

def parse_text(generator):
    """
    Filter the visible text from an html doc.

    Parameters
    ----------
    generator: `str`
        The html doc.

    Returns
    -------
    list[str]
    Visible text filtered from the html doc.
    """
    soup = BeautifulSoup(generator)
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
    as_str = str(element)
    if element.parent.name in NON_VISIBLE_LABELS:
        return False
    elif re.match('<!--.*-->', as_str):
        return False
    elif as_str == '\n':
        return False
    return True


