from django.conf import settings


def accounts(request):
    return {'SOCIAL_AUTH_ENABLED': settings.SOCIAL_AUTH_ENABLED}
