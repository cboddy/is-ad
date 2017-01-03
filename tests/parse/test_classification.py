import os.path
from is_ad.parse.classification import (
    _parse,
    parse_classifications
)


def test__parse():
    line = '845185_raw_html.txt,0\n'
    entry, is_ad = _parse(line)
    assert entry == '845185_raw_html.txt'
    assert not is_ad


def test_get_classifications():
    zip_path = os.path.join('tests','resources','train.csv.zip')
    classifications = parse_classifications(zip_path)
