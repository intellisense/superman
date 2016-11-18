from django.test import TestCase, override_settings
from django.core.urlresolvers import reverse, NoReverseMatch


class UrlsTest(TestCase):
    @override_settings(SOCIAL_AUTH_ENABLED=True)
    def test_valid(self):
        with not self.assertRaises(NoReverseMatch):
            reverse('social:begin', args=['google-oauth2'])

    @override_settings(SOCIAL_AUTH_ENABLED=False)
    def test_valid(self):
        with self.assertRaises(NoReverseMatch):
            reverse('social:begin', args=['google-oauth2'])
