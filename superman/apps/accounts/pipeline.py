from django.contrib.auth import get_user_model

from social.exceptions import SocialAuthBaseException


def load_user(*args, **kwargs):
    user = None
    response = kwargs.get('response', {})
    if response:
        emails = response.get('emails', [])
        for email in emails:
            if email['type'] == 'account':
                user = get_user_model().objects.filter(email__iexact=email['value']).first()
                if not user:
                    raise SocialAuthBaseException('User account does not exist.')
    return {'user': user, 'uid': user.id if user else None}
