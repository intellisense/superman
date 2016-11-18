from django.test import TestCase, override_settings

from ..context_processors import accounts


class ContextProcessorsTest(TestCase):
    @override_settings(SOCIAL_AUTH_ENABLED=True)
    def test_valid_1(self):
        data = accounts(None)
        self.assertTrue(data['SOCIAL_AUTH_ENABLED'])

    @override_settings(SOCIAL_AUTH_ENABLED=False)
    def test_valid_1(self):
        data = accounts(None)
        self.assertFalse(data['SOCIAL_AUTH_ENABLED'])
