from django.test import TestCase
from django.contrib.auth import get_user_model

from ..pipeline import load_user, SocialAuthBaseException


class PipelineTest(TestCase):
    def setUp(self):
        super(PipelineTest, self).setUp()
        self.User = get_user_model()
        self.user = self.User.objects.create(username='test', email='test@example.com')

    def test_no_response(self):
        data = load_user(response=None)
        self.assertEqual(data, {'user': None, 'uid': None})

    def test_empty_response(self):
        data = load_user(response={})
        self.assertEqual(data, {'user': None, 'uid': None})

    def test_response_with_different_type_of_email(self):
        data = load_user(response={'emails': [{'type': 'personal', 'value': self.user.email}]})
        self.assertEqual(data, {'user': None, 'uid': None})

    def test_response_with_valid_type_of_email(self):
        # valid email type is `account`
        data = load_user(response={'emails': [{'type': 'account', 'value': self.user.email}]})
        self.assertEqual(data, {'user': self.user, 'uid': self.user.id})

    def test_response_with_valid_type_of_email_but_no_account_exist(self):
        with self.assertRaises(SocialAuthBaseException):
            load_user(response={'emails': [{'type': 'account', 'value': 'test2@example.com'}]})
