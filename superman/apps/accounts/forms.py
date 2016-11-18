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

        self.old_iban = None
        if hasattr(self, 'instance') and hasattr(self.instance, 'pk') and self.instance.pk:
            self.old_iban = self.instance.iban

    def clean_iban(self):
        iban = self.cleaned_data.get('iban')
        if iban:
            if not self.old_iban or self.old_iban.lower() != iban.lower():
                if get_user_model().objects.filter(iban__iexact=iban).exists():
                    raise forms.ValidationError(_('User with this IBAN already exists.'))
        return iban


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
    class Meta(BaseUserChangeForm.Meta):
        model = get_user_model()
