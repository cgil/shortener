from shortener.lib import url_lib
from shortener.models.snippet import Snippet
from shortener.tests import factories
from shortener.tests.base import ViewTestCase


class SnippetTestCase(ViewTestCase):

    def setUp(self):
        super(SnippetTestCase, self).setUp()
        self.model_factory = factories.SnippetFactory
        self.model = Snippet

    def test_get_redirect_default(self):
        """Test that we can redirect to the default desktop url."""
        # set up a test record
        snippet = self.model_factory()
        snippet.short_url = url_lib.encode_short_url(snippet.id)
        snippet.save(snippet)
        res = self.raw_get(snippet.short_url)
        assert res.status_code == 302
        assert res.headers['Location'] == snippet.desktop_redirect

    def test_get_redirect_mobile(self):
        """Test that we can redirect to a specified mobile url."""
        # set up a test record
        mobile_redirect = 'https://mobile.com/mobile'
        snippet = self.model_factory(
            mobile_redirect=mobile_redirect,
        )
        snippet.short_url = url_lib.encode_short_url(snippet.id)
        snippet.save(snippet)
        res = self.raw_get(
            snippet.short_url,
            headers={'User-Agent': 'iphone'}
        )
        assert res.status_code == 302
        assert res.headers['Location'] == snippet.mobile_redirect

    def test_get_redirect_tablet(self):
        """Test that we can redirect to a specified tablet url."""
        # set up a test record
        tablet_redirect = 'https://www.tablet.com/tablet'
        snippet = self.model_factory(
            tablet_redirect=tablet_redirect
        )
        snippet.short_url = url_lib.encode_short_url(snippet.id)
        snippet.save(snippet)
        res = self.raw_get(
            snippet.short_url,
            headers={'User-Agent': 'ipad'}
        )
        assert res.status_code == 302
        assert res.headers['Location'] == snippet.tablet_redirect

    def test_get_redirect_desktop(self):
        """Test that we can redirect to a specified desktop url."""
        # set up a test record
        snippet = self.model_factory()
        snippet.short_url = url_lib.encode_short_url(snippet.id)
        snippet.save(snippet)
        res = self.raw_get(
            snippet.short_url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
            },
        )
        assert res.status_code == 302
        assert res.headers['Location'] == snippet.desktop_redirect

    def test_get_redirect_mobile_fallback(self):
        """Test that we can redirect to the default if not mobile url set."""
        # set up a test record
        snippet = self.model_factory(
            mobile_redirect=None,
        )
        snippet.short_url = url_lib.encode_short_url(snippet.id)
        snippet.save(snippet)
        res = self.raw_get(
            snippet.short_url,
            headers={'User-Agent': 'iphone'}
        )
        assert res.status_code == 302
        assert res.headers['Location'] == snippet.desktop_redirect

    def test_get_redirect_404(self):
        """Test that we can handle record 404's."""
        res = self.raw_get('http://localhost:5000/fakesnippet')
        assert res.status_code == 404
