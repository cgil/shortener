from shortener.models.snippet import Snippet
from shortener.tests.base import BaseTestCase


class SnippetTestCase(BaseTestCase):

    def test_snippet(self):
        """Test that we can create a snippet."""
        attrs = dict(
            mobile_redirect='http://mobile.com',
            tablet_redirect='http://tablet.com',
            desktop_redirect='http://desktop.com',
        )
        snippet = Snippet(**attrs)
        snippet.save(snippet)
        res = Snippet.get(snippet.id)
        for attr in attrs:
            assert getattr(res, attr) == attrs[attr]
        assert snippet.mobile_redirect_count == 0
        assert snippet.desktop_redirect_count == 0
        assert snippet.tablet_redirect_count == 0
