from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTest(TestCase):
    def test_creation(self):
        u = get_user_model().objects.create(username='test')
        self.assertEqual(u.__str__(), u.username)

        u.first_name = 'John'
        u.save()
        self.assertEqual(u.__str__(), u.first_name)

        u.last_name = 'Doe'
        u.save()
        self.assertEqual(u.__str__(), '{0} {1}'.format(u.first_name, u.last_name))
