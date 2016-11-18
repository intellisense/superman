from django.contrib.admin.sites import AdminSite
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from ..admin import UserAdmin


class MockRequest(object):
    pass


request = MockRequest()


class UserAdminTest(TestCase):
    def setUp(self):
        super(TestCase, self).setUp()
        self.site = AdminSite()
        self.User = get_user_model()
        # super user
        self.super_user = self.User.objects.create(username='admin', is_superuser=True)
        # staff users
        self.staff_user_1 = self.User.objects.create(username='staff1', is_staff=True)
        self.staff_user_2 = self.User.objects.create(username='staff2', is_staff=True)
        # adjust permissions
        content_type = ContentType.objects.get_for_model(self.User)
        change_perm = Permission.objects.get(codename='change_user', content_type__id=content_type.id)
        delete_perm = Permission.objects.get(codename='delete_user', content_type__id=content_type.id)
        self.staff_user_1.user_permissions.add(change_perm, delete_perm)
        self.staff_user_2.user_permissions.add(change_perm, delete_perm)

        # test users
        self.test_user_1 = self.User.objects.create(username='test1', created_by=self.staff_user_1)
        self.test_user_2 = self.User.objects.create(username='test2', created_by=self.staff_user_2)

    def test_queryset(self):
        ma = UserAdmin(self.User, self.site)

        # superuser can see all users
        request.user = self.super_user
        qs = ma.get_queryset(request)
        self.assertEqual(qs.count(), 5)

        # staff user can only those users crated by him
        request.user = self.staff_user_1
        qs = ma.get_queryset(request)
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs[0].username, 'test1')

        request.user = self.staff_user_2
        qs = ma.get_queryset(request)
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs[0].username, 'test2')

    def test_get_form(self):
        ma = UserAdmin(self.User, self.site)

        # staff users don't see sensitive fields in change form
        request.user = self.staff_user_1
        form = ma.get_form(request, obj=self.test_user_1)
        self.assertEqual(form._meta.fields, ['username', 'password', 'first_name',
                                             'last_name', 'email', 'iban',
                                             'is_active', 'last_login', 'date_joined'])

        # superuser users can see all fields
        request.user = self.super_user
        form = ma.get_form(request, obj=self.test_user_1)
        self.assertEqual(form._meta.fields, ['username', 'password', 'first_name',
                                             'last_name', 'email', 'iban',
                                             'is_active', 'is_staff', 'is_superuser',
                                             'groups', 'user_permissions', 'created_by',
                                             'last_login', 'date_joined'])

    def test_get_list_display(self):
        ma = UserAdmin(self.User, self.site)

        # for superuser
        request.user = self.super_user
        list_display = ma.get_list_display(request)
        self.assertEqual(list_display, ('username', 'first_name', 'last_name', 'iban',
                                        'is_staff', 'is_superuser', 'is_active', 'created_by'))

        # for staff user
        request.user = self.staff_user_1
        list_display = ma.get_list_display(request)
        self.assertEqual(list_display, ('username', 'first_name', 'last_name', 'iban', 'is_active'))

    def test_get_list_filter(self):
        ma = UserAdmin(self.User, self.site)

        # for superuser
        request.user = self.super_user
        list_filter = ma.get_list_filter(request)
        self.assertEqual(list_filter, ('is_staff', 'is_superuser', 'is_active',
                                       'date_joined', 'created_by'))

        # for staff user
        request.user = self.staff_user_1
        list_filter = ma.get_list_filter(request)
        self.assertEqual(list_filter, ('is_active', 'date_joined'))

    def test_has_permission(self):
        # restrict manipulation operation to the administrators who created them
        # unless superuser
        ma = UserAdmin(self.User, self.site)

        # superuser
        request.user = self.super_user
        has_permission = ma.has_permission(request, self.test_user_1)
        self.assertTrue(has_permission)

        # staff user permission on test user created by him
        request.user = self.staff_user_1
        has_permission = ma.has_permission(request, self.test_user_1)
        self.assertTrue(has_permission)

        # staff user permission on test user not created by him
        request.user = self.staff_user_1
        has_permission = ma.has_permission(request, self.test_user_2)
        self.assertFalse(has_permission)

    def test_has_change_permission(self):
        ma = UserAdmin(self.User, self.site)

        # superuser
        request.user = self.super_user
        has_permission = ma.has_change_permission(request, self.test_user_1)
        self.assertTrue(has_permission)

        has_permission = ma.has_change_permission(request)
        self.assertTrue(has_permission)

        # staff user permission on test user created by him
        request.user = self.staff_user_1
        has_permission = ma.has_change_permission(request, self.test_user_1)
        self.assertTrue(has_permission)

        has_permission = ma.has_change_permission(request)
        self.assertTrue(has_permission)

        # staff user permission on test user not created by him
        request.user = self.staff_user_1
        has_permission = ma.has_change_permission(request, self.test_user_2)
        self.assertFalse(has_permission)

    def test_has_delete_permission(self):
        ma = UserAdmin(self.User, self.site)

        # superuser
        request.user = self.super_user
        has_permission = ma.has_delete_permission(request, self.test_user_1)
        self.assertTrue(has_permission)

        has_permission = ma.has_delete_permission(request)
        self.assertTrue(has_permission)

        # staff user permission on test user created by him
        request.user = self.staff_user_1
        has_permission = ma.has_delete_permission(request, self.test_user_1)
        self.assertTrue(has_permission)

        has_permission = ma.has_delete_permission(request)
        self.assertTrue(has_permission)

        # staff user permission on test user not created by him
        request.user = self.staff_user_1
        has_permission = ma.has_delete_permission(request, self.test_user_2)
        self.assertFalse(has_permission)
