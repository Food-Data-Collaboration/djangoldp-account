from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseNotFound
from django.views import View
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse
from djangoldp_account import settings

from djangoldp_account.endpoints.rp_login import RPLoginCallBackEndpoint, RPLoginEndpoint
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


def check_user(request, *args, **kwargs):
    if request.method == 'OPTIONS':
        response = HttpResponse({}, status=200)
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = 'Authorization'
        response['Cache-Control'] = 'no-store'
        response['Pragma'] = 'no-cache'

        return response

    if request.user.is_authenticated():
        response = JsonResponse(settings.userinfo({}, request.user))
        try:
            response['User'] = request.user.webid()
        except AttributeError:
            pass
        return response
    else :
        return HttpResponseNotFound()


class RedirectView(View):
    """
    View for managing where to redirect the user after a successful login
    In the event that 'next' is not set (they may be coming from one of multiple front-end apps)

    To use this functionality set LOGIN_REDIRECT_URL to a url which uses this View. Then if the user
    has not set 'next' parameter in the login request, Django will redirect them here
    """
    def get(self, request, *args, **kwargs):
        next = request.user.default_redirect_uri

        # attempt to redirect to the user's default_redirect_uri
        if next is not None and next != '':
            return redirect(next, permanent=False)

        # there is no default to fall back on
        # redirect admins to the admin panel
        if request.user.is_superuser:
            return redirect(reverse('admin:index'), permanent=False)

        # redirect other users to a page apologising
        return render(request, template_name='registration/lost_user.html')


class LDPAccountLoginView(LoginView):
    """
    Extension of django.contrib.auth.views.LoginView for managing user's default_redirect_uri
    """
    # Save login url as preferred redirect
    def post(self, request, *args, **kwargs):
        from django.conf import settings

        return_value = super(LDPAccountLoginView, self).post(request, *args, **kwargs)

        # if the user has 'next' set which is not default, update their preference
        next = request.POST.get('next')
        if next != settings.LOGIN_REDIRECT_URL:
            request.user.default_redirect_uri = next
            request.user.save()

        return return_value


class RPLoginView(View):
    """
    RP authentication workflow
    See https://github.com/solid/webid-oidc-spec/blob/master/example-workflow.md
    Wa're using oid module : https://pyoidc.readthedocs.io/en/latest/examples/rp.html
    """
    endpoint_class = RPLoginEndpoint

    def get(self, request, *args, **kwargs):
        return self.on_request(request)

    def on_request(self, request):
        endpoint = self.endpoint_class(request)
        try:
            endpoint.validate_params()

            return HttpResponseRedirect(endpoint.op_login_url())

        except LDPLoginError as error:
            return JsonResponse(error.create_dict(), status=400)

    def post(self, request, *args, **kwargs):
        return self.on_request(request)


class RPLoginCallBackView(View):
    endpoint_class = RPLoginCallBackEndpoint

    def get(self, request, *args, **kwargs):
        return self.on_request(request)

    def on_request(self, request):
        endpoint = self.endpoint_class(request)
        try:
            endpoint.validate_params()

            return HttpResponseRedirect(endpoint.initial_url())

        except LDPLoginError as error:
            return JsonResponse(error.create_dict(), status=400)

    def post(self, request, *args, **kwargs):
        return self.on_request(request)
