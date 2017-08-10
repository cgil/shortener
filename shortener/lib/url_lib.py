from shortener.utils import base62
from shortener.utils.configuration import config


def encode_short_url(num):
    """Encodes a number into a short url."""
    base_url = config.get('short_url.base')
    encoded_domain = base62.encode(num)
    short_url = '{}/{}'.format(base_url, encoded_domain)
    return short_url


def decode_short_url(short_url):
    """Decodes a short url into its original index number."""
    encoded_short_url = short_url.split('/')[-1]
    decoded_num = base62.decode(encoded_short_url)
    return decoded_num
