"""
Base 62 (configurable) encoder and decoder based on:
    https://gist.github.com/adyliu/4494223
"""

BASE_CHARS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
BASE = len(BASE_CHARS)


def decode(s):
    """Decodes a Base62 string into a base10 number."""
    ret, mult = 0, 1
    for c in reversed(s):
        ret += mult * BASE_CHARS.index(c)
        mult *= BASE
    return ret


def encode(num):
    """Encodes a number into base 62."""
    if num < 0:
        raise Exception('positive number ' + num)
    if num == 0:
        return '0'
    ret = ''
    while num != 0:
        ret = (BASE_CHARS[num % BASE]) + ret
        num = num // BASE
    return ret
