import os.path

from ad_finder.parse.html import (
    parse_texts,
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
    text_elements = parse_texts(html_doc)
    assert text_elements == ['Hello!', 'Isad']


def test_parse_zip():
    zip_path =os.path.join('tests',  'resources', '0.test.zip')
    has_entry = [False]

    def test_consumer(name, text):
        assert name == '0/1000188_raw_html.txt'
        assert len(text) == 165
        has_entry[0] = True

    parse_zip(zip_path, test_consumer)
    assert has_entry[0]


def test_profile_parse_zip():
    zip_path = os.path.join('/', 'home', 'chrirs', 'Downloads', 'dato.native', '0.zip')
    count = [0]
    def print_consumer(name, text):
        count[0]+=1
        if count[0] > 100:
            raise Exception('Done')
        print(name)

    parse_zip(zip_path, print_consumer)

# try :
test_profile_parse_zip()
# except Exception:
#     pass
