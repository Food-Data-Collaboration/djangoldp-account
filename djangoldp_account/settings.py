import validators
from django.conf import settings
from django.urls import reverse_lazy


def userinfo(claims, user):
    # Populate claims dict.
    claims['name'] = '{0} {1}'.format(user.first_name, user.last_name)
    claims['email'] = user.email
    claims['website'] = user.webid()
    claims['webid'] = user.webid()
    return claims
