from django.test import TestCase
from django.contrib.auth import get_user_model

from ..utils import generate_unique_username


class AutoUsernameTest(TestCase):
    def setUp(self):
        super(AutoUsernameTest, self).setUp()
        self.User = get_user_model()

    def test_auto_username_from_empty_list(self):
        # no matter what `generate_unique_username` should return random username
        username = generate_unique_username([])
        self.assertNotEqual(username, '')
        self.assertNotEqual(username, None)

    def test_auto_username_from_empty_parts(self):
        # no matter what `generate_unique_username` should return random username
        username = generate_unique_username([''])
        self.assertNotEqual(username, '')
        self.assertNotEqual(username, None)

    def test_auto_username_from_parts(self):
        username = generate_unique_username(['John'])
        self.assertEqual(username, 'john')

    def test_auto_username_length(self):
        # username generated should never exceeds max_length
        max_length = self.User._meta.get_field(self.User.USERNAME_FIELD).max_length
        # lets use a string which is greater than max_length
        username = generate_unique_username(['a'*(max_length+10)])
        self.assertLessEqual(len(username), max_length)

    def test_auto_username_sanity(self):
        # if username already exists in system the conflict should be resolved
        self.User.objects.create(username='john')
        username = generate_unique_username(['John'])
        self.assertEqual(username, 'john2')
