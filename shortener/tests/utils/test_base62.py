from shortener.tests.base import BaseTestCase
from shortener.utils import base62


class Base62TestCase(BaseTestCase):

    def test_encode(self):
        """Test encoding a number into base62."""
        assert base62.encode(1) == '1'
        assert base62.encode(10) == 'a'
        assert base62.encode(61) == 'Z'
        assert base62.encode(62) == '10'
        assert base62.encode(100) == '1C'
        assert base62.encode(1234567891234567891) == '1tckI30s18v'

    def test_decode(self):
        """Test decoding a base62 string to a number."""
        assert base62.decode('1') == 1
        assert base62.decode('a') == 10
        assert base62.decode('Z') == 61
        assert base62.decode('10') == 62
        assert base62.decode('1tckI30s18v') == 1234567891234567891
