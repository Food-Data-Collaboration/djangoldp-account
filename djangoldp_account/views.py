from oidc_provider.views import userinfo
from django.http import HttpResponse

import requests

def userinfocustom(request, *args, **kwargs):
    if request.method == 'OPTIONS':

        response = HttpResponse({}, status=200)
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = 'Authorization'
        response['Cache-Control'] = 'no-store'
        response['Pragma'] = 'no-cache'

        return response

    return userinfo(request, *args, **kwargs)

