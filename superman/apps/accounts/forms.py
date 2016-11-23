from django import forms
from django.contrib.auth.forms import (
    UserCreationForm as BaseUserCreationForm,
    UserChangeForm as BaseUserChangeForm)
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from .utils import generate_unique_username


class BaseUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseUserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

        self.fields['iban'].label = _('IBAN')
        if not self.user.is_superuser:
            # non superuser can't add users without IBAN
            self.fields['iban'].required = True
        else:
            self.fields['iban'].required = False

        self.old_email = None
        if hasattr(self, 'instance') and hasattr(self.instance, 'pk') and self.instance.pk:
            self.old_email = self.instance.email

    def clean_iban(self):
        """
        if IBAN is empty string return None instead
        """
        return self.cleaned_data.get('iban') or None


class UserCreationForm(BaseUserCreationForm, BaseUserForm):
    def save(self, **kwargs):
        commit = kwargs.get('commit', False)
        kwargs['commit'] = False
        user = super(UserCreationForm, self).save(**kwargs)
        # set auto username
        user.username = generate_unique_username([user.first_name, user.last_name])
        # set user who is creating this new user
        user.created_by = self.user
        if commit:
            user.save()
        return user

    class Meta(BaseUserCreationForm.Meta):
        fields = ('first_name', 'last_name', 'iban')
        model = get_user_model()


class UserChangeForm(BaseUserChangeForm, BaseUserForm):
    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        if not self.user.is_superuser:
            self.fields.pop('is_staff', None)
            self.fields.pop('is_superuser', None)
            self.fields.pop('created_by', None)
            self.fields.pop('groups', None)
            self.fields.pop('user_permissions', None)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            if not self.old_email or self.old_email.lower() != email.lower():
                if get_user_model().objects.filter(email__iexact=email).exists():
                    raise forms.ValidationError(_('User with this email already exists.'))
        return email

    class Meta(BaseUserChangeForm.Meta):
        model = get_user_model()
