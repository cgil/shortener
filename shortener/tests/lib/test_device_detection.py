from shortener.lib import device_detection as dd
from shortener.tests.base import BaseTestCase


class DeviceDetectionTestCase(BaseTestCase):

    def test_detect_mobile(self):
        """Test detecting mobile devices."""
        mobile_user_agents = [
            'iphone', 'ipod', 'android mobile', 'windows phone',
            'dream', 'blackberry', 'cupcake', 'webos', 'incognito', 'webmate'
        ]
        for v in mobile_user_agents:
            assert dd.detect(FakeRequest(v)) == dd.MOBILE

    def test_detect_tablet(self):
        """Test detecting tablet devices."""
        tablet_user_agents = ['ipad', 'android']
        for v in tablet_user_agents:
            assert dd.detect(FakeRequest(v)) == dd.TABLET

    def test_detect_desktop(self):
        """Test detecting desktop devices."""
        desktop_user_agents = ['Mozilla', 'other']
        for v in desktop_user_agents:
            assert dd.detect(FakeRequest(v)) == dd.DESKTOP


class FakeUserAgent(object):

    def __init__(self, user_agent):
        self.string = user_agent


class FakeRequest(object):

    def __init__(self, user_agent):
        self.user_agent = FakeUserAgent(user_agent)
