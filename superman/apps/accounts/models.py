from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from localflavor.generic.models import IBANField


class User(AbstractUser):
    iban = IBANField(_('IBAN'), null=True, blank=True)
    created_by = models.ForeignKey('self', null=True, blank=True,
                                   on_delete=models.SET_NULL, related_name='owned_users')

    def __str__(self):
        return self.get_full_name() or self.get_username()
