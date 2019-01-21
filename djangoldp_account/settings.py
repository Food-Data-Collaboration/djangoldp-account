from django.conf import settings
from django.urls import reverse_lazy


def userinfo(claims, user):
    # Populate claims dict.
    claims['name'] = '{0} {1}'.format(user.first_name, user.last_name)
    claims['email'] = user.email
    claims['website'] = '{0}{1}'.format(settings.BASE_URL, reverse_lazy('user-detail', kwargs={'pk': user.pk}))
    return claims

