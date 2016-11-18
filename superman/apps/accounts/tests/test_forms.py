from django.test import TestCase
from django.contrib.auth import get_user_model

from ..forms import UserCreationForm, UserChangeForm


class Helper(TestCase):
    def setUp(self):
        super(Helper, self).setUp()
        self.User = get_user_model()
        self.super_user = self.User.objects.create(username='admin', is_superuser=True)
        self.staff_user = self.User.objects.create(username='staff', is_staff=True)


class UserCreationFormTest(Helper):
    def setUp(self):
        super(UserCreationFormTest, self).setUp()
        self.form = UserCreationForm
        self.first_name = 'john'
        self.last_name = 'doe'
        self.data = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'password1': 'superman!@#',
            'password2': 'superman!@#',
        }
        self.iban = 'DE44500105175407324931'

    def test_fields_for_superuser(self):
        # first_name, last_name and password1 and password2 are always required
        self.form.user = self.super_user
        form = self.form()
        # test required fields
        self.assertEqual([f for f in form.fields if form.fields[f].required],
                         ['first_name', 'last_name', 'password1', 'password2'])
        # test non required fields
        self.assertEqual([f for f in form.fields if not form.fields[f].required], ['iban'])

    def test_fields_for_staffuser(self):
        # first_name, last_name and password1 and password2 are always required
        self.form.user = self.staff_user
        form = self.form()
        # test required fields
        self.assertEqual([f for f in form.fields if form.fields[f].required],
                         ['first_name', 'last_name', 'iban', 'password1', 'password2'])
        # test non required fields
        self.assertEqual([f for f in form.fields if not form.fields[f].required], [])

    def test_valid_data_for_super_user_without_iban(self):
        self.form.user = self.super_user
        form = self.form(self.data)
        self.assertTrue(form.is_valid())
        user = form.save(commit=True)
        self.assertEqual(user.first_name, self.first_name)
        self.assertEqual(user.last_name, self.last_name)
        self.assertNotEqual(user.username, None)
        self.assertNotEqual(user.created_by, None)
        self.assertEqual(user.created_by.id, self.super_user.id)

    def test_valid_data_for_super_user_with_iban(self):
        self.form.user = self.super_user
        self.data['iban'] = self.iban
        form = self.form(self.data)
        self.assertTrue(form.is_valid())
        user = form.save(commit=True)
        self.assertEqual(user.first_name, self.first_name)
        self.assertEqual(user.last_name, self.last_name)
        self.assertNotEqual(user.username, None)
        self.assertNotEqual(user.created_by, None)
        self.assertEqual(user.created_by.id, self.super_user.id)

    def test_valid_data_for_staff_user(self):
        self.form.user = self.staff_user
        self.data['iban'] = self.iban
        form = self.form(self.data)
        self.assertTrue(form.is_valid())
        user = form.save(commit=True)
        self.assertEqual(user.first_name, self.first_name)
        self.assertEqual(user.last_name, self.last_name)
        self.assertNotEqual(user.username, None)
        self.assertNotEqual(user.created_by, None)
        self.assertEqual(user.created_by.id, self.staff_user.id)

    def test_invalid_data(self):
        self.form.user = self.super_user  # doesn't matter which user

        # empty data
        form = self.form({})
        self.assertFalse(form.is_valid())

        # required field `first_name` missing
        data = self.data.copy()
        del data['first_name']
        form = self.form(data)
        self.assertFalse(form.is_valid())

        # required field `last_name` missing
        data = self.data.copy()
        del data['last_name']
        form = self.form(data)
        self.assertFalse(form.is_valid())

        # required field `password1` missing
        data = self.data.copy()
        del data['password1']
        form = self.form(data)
        self.assertFalse(form.is_valid())

        # required field `password2` missing
        data = self.data.copy()
        del data['password2']
        form = self.form(data)
        self.assertFalse(form.is_valid())

        # password mismatch
        data = self.data.copy()
        data['password2'] = 'blah'
        form = self.form(data)
        self.assertFalse(form.is_valid())

        # invalid IBAN
        data = self.data.copy()
        data['iban'] = 'blah'
        form = self.form(data)
        self.assertFalse(form.is_valid())

        # IBAN already exists
        self.User.objects.create(username='test_user', iban=self.iban)
        data = self.data.copy()
        data['iban'] = self.iban
        form = self.form(data)
        self.assertFalse(form.is_valid())


class UserChangeFormTest(Helper):
    def setUp(self):
        super(UserChangeFormTest, self).setUp()
        self.form = UserChangeForm
        self.data = {
            'username': 'john_doe',
            'first_name': 'John',
            'last_name': 'Doe',
        }
        self.normal_user = self.User.objects.create(**self.data)
        self.iban = 'DE44500105175407324931'

    def test_fields_for_superuser(self):
        # first_name, last_name are always required
        self.form.user = self.super_user
        form = self.form(instance=self.normal_user)
        # test required fields
        self.assertEqual([f for f in form.fields if form.fields[f].required],
                         ['username', 'first_name', 'last_name', 'date_joined'])

    def test_fields_for_staffuser(self):
        # first_name, last_name and iban are always required
        self.form.user = self.staff_user
        form = self.form(instance=self.normal_user)
        # test required fields
        self.assertEqual([f for f in form.fields if form.fields[f].required],
                         ['username', 'first_name', 'last_name', 'date_joined', 'iban'])

    def test_invalid_data(self):
        self.form.user = self.super_user  # doesn't matter which user

        # empty data
        form = self.form({}, instance=self.normal_user)
        self.assertFalse(form.is_valid())

        # required field `first_name` missing
        data = self.data.copy()
        del data['first_name']
        form = self.form(data, instance=self.normal_user)
        self.assertFalse(form.is_valid())

        # required field `last_name` missing
        data = self.data.copy()
        del data['last_name']
        form = self.form(data, instance=self.normal_user)
        self.assertFalse(form.is_valid())

        # invalid IBAN
        data = self.data.copy()
        data['iban'] = 'blah'
        form = self.form(data, instance=self.normal_user)
        self.assertFalse(form.is_valid())

        u = self.User.objects.create(username='test_user', iban=self.iban, email='test@example.com')
        # IBAN already exists
        data = self.data.copy()
        data['iban'] = u.iban
        form = self.form(data, instance=self.normal_user)
        self.assertFalse(form.is_valid())

        # email belong to another user
        data = self.data.copy()
        data['email'] = u.email
        form = self.form(data, instance=self.normal_user)
        self.assertFalse(form.is_valid())

        # username belong to another user
        data = self.data.copy()
        data['username'] = u.username
        form = self.form(data, instance=self.normal_user)
        self.assertFalse(form.is_valid())

    def test_valid_data(self):
        self.form.user = self.staff_user

        username = 'new_username'
        first_name = 'new_first_name'
        last_name = 'new_last_name'
        email = 'new_email@example.com'

        data = {
            'iban': self.iban,
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'date_joined': self.normal_user.date_joined,
        }
        form = self.form(data, instance=self.normal_user)
        self.assertTrue(form.is_valid())
        user = form.save(commit=True)
        self.assertEqual(user.username, username)
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertEqual(user.email, email)
        self.assertEqual(user.iban, self.iban)

    def test_sanity(self):
        """
        Staff user can't make another user superuser or staff user, or change created_by
        """
        self.form.user = self.staff_user
        self.data['is_superuser'] = True
        self.data['is_staff'] = True
        self.data['date_joined'] = self.normal_user.date_joined
        self.data['iban'] = self.iban
        self.data['created_by'] = self.super_user
        form = self.form(self.data, instance=self.normal_user)
        self.assertTrue(form.is_valid())
        user = form.save(commit=True)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.created_by, None)
