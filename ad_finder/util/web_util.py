import urllib2

HEADERS = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"} # nothing to see here


def get(url, timeout=10):
    """HTTP GET url resource."""
    request = urllib2.Request(url, headers=HEADERS)
    response = urllib2.urlopen(request, timeout=timeout)
    try:
        return response.read()
    finally:
        response.close()

