import os.path

from ad_finder.parse.zip_util import zip_open
from ad_finder.parse.html import (
    _is_visible,
    parse_text,
    parse_zip
)

def test_parse_text():
    html_doc = '''
    <body>
    <script>blah</script>
    <p>Hello isad.</p>
    </body>
    '''
    text_elements = parse_text(html_doc)
    assert text_elements == ['Hello isad.']

