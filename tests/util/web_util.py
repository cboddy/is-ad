from is_ad.util.web_util import get


def test_get():
    page = get('http://example.com')
    assert len(page) == 1270
