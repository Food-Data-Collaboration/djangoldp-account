from django.http import HttpResponse, JsonResponse
from django.views import View

from djangoldp_account.endpoints.login import RLLoginEndpoint
from djangoldp_account.errors import LDPLoginError
from oic.utils.http_util import Redirect
from oidc_provider.views import userinfo


def userinfocustom(request, *args, **kwargs):
    if request.method == 'OPTIONS':
        response = HttpResponse({}, status=200)
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = 'Authorization'
        response['Cache-Control'] = 'no-store'
        response['Pragma'] = 'no-cache'

        return response

    return userinfo(request, *args, **kwargs)


class RLLoginView(View):
    """
    RL authentication workflow
    See https://github.com/solid/webid-oidc-spec/blob/master/example-workflow.md
    Wa're using oid module : https://pyoidc.readthedocs.io/en/latest/examples/rp.html
    """
    login_endpoint_class = RLLoginEndpoint

    def get(self, request, *args, **kwargs):
        return self.on_request(request)

    def on_request(self, request):
        login = self.login_endpoint_class(request)
        try:
            login.validate_params()

            return Redirect(login.op_login_url())

        except LDPLoginError as error:
            return JsonResponse(error.create_dict(), status=400)

    def post(self, request, *args, **kwargs):
        return self.on_request(request)


class RLLoginCallBackView(View):

    def get(self, request, *args, **kwargs):

        try:
            pass
        except:
            pass
