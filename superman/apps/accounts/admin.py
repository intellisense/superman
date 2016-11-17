from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User
from .forms import UserCreationForm, UserChangeForm


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'iban')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Administration'), {'fields': ('created_by', )}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    original_fieldsets = fieldsets
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'iban', 'password1', 'password2'),
        }),
    )
    add_form = UserCreationForm
    form = UserChangeForm
    list_display = ('username', 'first_name', 'last_name', 'iban',
                    'is_staff', 'is_superuser', 'is_active', 'created_by')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined', 'created_by')
    raw_id_fields = ('created_by', )

    def get_form(self, request, obj=None, **kwargs):
        user = request.user
        if obj and not user.is_superuser:
            # for simple administrators who are not superuser we need to hide sensitive fields
            self.exclude = ('is_staff', 'is_superuser', 'created_by', 'groups', 'user_permissions')
            self.fieldsets = (
                (None, {'fields': ('username', 'password')}),
                (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'iban')}),
                (_('Permissions'), {'fields': ('is_active', )}),
                (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
            )
        else:
            self.exclude = None
            self.fieldsets = self.original_fieldsets
        form = super(UserAdmin, self).get_form(request, obj=obj, **kwargs)
        form.user = user
        return form

    def get_list_display(self, request):
        """
        For simple administrators who are not superuser we only need to show relevant columns
        """
        if not request.user.is_superuser:
            list_display = ('username', 'first_name', 'last_name', 'iban', 'is_active')
            return list_display
        return super(UserAdmin, self).get_list_display(request)

    def get_list_filter(self, request):
        """
        For simple administrators who are not superuser we only need to show relevant filters
        """
        if not request.user.is_superuser:
            list_filter = ('is_active', 'date_joined')
            return list_filter
        return super(UserAdmin, self).get_list_filter(request)

    def has_permission(self, request, obj=None):
        """
        If user is not superuser then check request.user is the one who created the user `obj`
        :param request: Http request
        :param obj: accounts.User object
        :return: boolean
        """
        has_perm = True
        user = request.user
        if obj and not user.is_superuser:
            created_by = obj.created_by
            if not created_by or created_by.id != user.id:
                has_perm = False
        return has_perm

    def has_change_permission(self, request, obj=None):
        if not self.has_permission(request, obj=obj):
            return False
        return super(UserAdmin, self).has_change_permission(request, obj=obj)

    def has_delete_permission(self, request, obj=None):
        if not self.has_permission(request, obj=obj):
            return False
        return super(UserAdmin, self).has_delete_permission(request, obj=obj)

    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by__id=request.user.id)
