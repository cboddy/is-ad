import os.path

from ad_finder.parse.zip_util import zip_open
from ad_finder.parse.html import (
    parse_text,
    parse_zip
)


def test_parse_text():
    html_doc = '''
    <body>
    <script>blah</script>
    <p>Hello!<p>
    <p>Isad</p>
    </body>
    '''
    text_elements = parse_text(html_doc)
    assert text_elements == ['Hello!', 'Isad']


def test_parse_zip():
    zip_path =os.path.join('tests',  'resources', '0.test.zip')
    parse_zip(zip_path)