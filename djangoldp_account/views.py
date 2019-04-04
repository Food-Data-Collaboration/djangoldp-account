from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views import View
from oic.oic import AuthorizationResponse

from djangoldp_account.endpoints.login import RPLoginEndpoint
from djangoldp_account.errors import LDPLoginError
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


class RPLoginView(View):
    """
    RP authentication workflow
    See https://github.com/solid/webid-oidc-spec/blob/master/example-workflow.md
    Wa're using oid module : https://pyoidc.readthedocs.io/en/latest/examples/rp.html
    """
    login_endpoint_class = RPLoginEndpoint

    def get(self, request, *args, **kwargs):
        return self.on_request(request)

    def on_request(self, request):
        login = self.login_endpoint_class(request)
        try:
            login.validate_params()

            return HttpResponseRedirect(login.op_login_url())

        except LDPLoginError as error:
            return JsonResponse(error.create_dict(), status=400)

    def post(self, request, *args, **kwargs):
        return self.on_request(request)


class RPLoginCallBackView(View):

    def get(self, request, *args, **kwargs):

        response = request.environ["QUERY_STRING"]

        # aresp = client.parse_response(AuthorizationResponse, info=response,
        #                               sformat="urlencoded")
        #
        # code = aresp["code"]
        # assert aresp["state"] == request.session['state']
        try:
            pass
        except:
            pass
