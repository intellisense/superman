from django.utils.deprecation import MiddlewareMixin

from social.apps.django_app.middleware import (
    SocialAuthExceptionMiddleware as BaseSocialAuthExceptionMiddleware)


class SocialAuthExceptionMiddleware(BaseSocialAuthExceptionMiddleware, MiddlewareMixin):
    # fix middleware, Middleware factories must accept a `get_response` argument
    pass
