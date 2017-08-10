"""Based on https://github.com/yasunori/flask-devices"""

import re

DESKTOP = 'desktop'
MOBILE = 'mobile'
TABLET = 'tablet'
PATTERNS = [
    (
        MOBILE,
        re.compile(
            r'iphone|ipod|android.*mobile|windows.*phone|dream'
            '|blackberry|cupcake|webos|incognito|webmate'
        )
    ),
    (TABLET, re.compile(r'ipad|android')),
    (DESKTOP, re.compile(r'.*')),
]


def detect(request):
    """Detect the device type by searching the user agent for known device strings."""
    user_agent = request.user_agent.string.lower()
    match = [(key, pattern) for key, pattern in PATTERNS if pattern.search(user_agent) is not None]
    return match[0][0]
