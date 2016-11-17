import re
import unicodedata

from django.utils.encoding import force_text
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string


USERNAME_RE = re.compile('[^\w\s@+.-]')


def _generate_unique_username_base(txts, regex=USERNAME_RE):
    username = None
    for txt in txts:
        if not txt:
            continue
        username = unicodedata.normalize('NFKD', force_text(txt))
        username = username.encode('ascii', 'ignore').decode('ascii')
        username = force_text(regex.sub('', username).lower())
        # only take the part leading up to the '@' as we already have email field.
        username = username.split('@')[0]
        username = username.strip()
        username = re.sub('\s+', '_', username)
        if username:
            break
    return username or None


def generate_unique_username(txts, regex=USERNAME_RE):
    """
    Generates a unique username from list of strings
    Code taken from django-allauth package with custom additional improvements:
      https://github.com/pennersr/django-allauth/blob/master/allauth/utils.py#L63
    :param txts: list of strings to generate username from
    :param regex: regex to validate username
    :return: unique username
    """
    User = get_user_model()
    max_length = User._meta.get_field(User.USERNAME_FIELD).max_length
    username = _generate_unique_username_base(txts, regex)
    if not username:
        username = get_random_string(max_length).lower()
    i = 0
    while True:
        try:
            if i:
                pfx = str(i + 1)
            else:
                pfx = ''
            ret = username[0:max_length - len(pfx)] + pfx
            query = {User.USERNAME_FIELD + '__iexact': ret}
            User.objects.get(**query)
            i += 1
        except User.DoesNotExist:
            return ret
