from shortener.lib import url_lib
from shortener.tests.base import BaseTestCase


class UrlLibTestCase(BaseTestCase):

    def test_encode_short_url(self):
        """Test encoding a number into a short url."""
        assert url_lib.encode_short_url(123) == 'http://localhost:5000/1Z'
        assert url_lib.encode_short_url(123456) == 'http://localhost:5000/w7e'

    def test_decode_short_url(self):
        """Test decoding a short url to the original index number."""
        assert url_lib.decode_short_url('http://localhost:5000/1Z') == 123
        assert url_lib.decode_short_url('http://localhost:5000/w7e') == 123456
