import validators
from django.conf import settings
from django.urls import reverse
from oic import rndstr
from requests import session

from djangoldp_account.errors import LDPLoginError
from oic.oic import Client
from oic.utils.authn.client import CLIENT_AUTHN_METHOD


class RLLoginEndpoint(object):
    """
    RL login endpoint
    This is *not* the OP login endpoint (OP part is managed by django_oidc)
    """
    client_class = Client

    def __init__(self, request):
        self.request = request
        self.params = {}

        self._extract_params()
        self.client = self.client_class(client_authn_method=CLIENT_AUTHN_METHOD)

    def _extract_params(self):
        """
        """
        # Because in this endpoint we handle both GET
        # and POST request.
        query_dict = (self.request.POST if self.request.method == 'POST'
                      else self.request.GET)

        self.params['subject'] = query_dict.get('subject', '')
        self.params['next'] = query_dict.get('next', '')

    def validate_params(self):
        """
        A provider must be set.
        It can be a url (auth provider)
        or email or webId (In those case, provider discovery is necessary)

        See: 2.1 https://github.com/solid/webid-oidc-spec/blob/master/example-workflow.md
        """

        if not validators.url(self.params['subject']) and not validators.email(self.params['subject']):
            raise LDPLoginError('invalid_request')

    def op_login_url(self):
        subject = self.params['subject']
        try:
            issuer = self.client.discover(subject)
            provider_info = self.client.provider_config(issuer)
        except:
            # assume that the subject is the provider
            try:
                provider_info = self.client.provider_config(subject)
            except:
                raise LDPLoginError("cannot_get_provider_info")

        is_register = False # TODO check if the server is already registered
        if not is_register:
            try:
                registration_endpoint = provider_info._dict["registration_endpoint"]
                args = {
                    "redirect_uris": [settings.SITE_URL + reverse('djangoldp_account:ldp_login_call_back')],
                    "contacts": ["foo@example.com"]
                }

                registration_response = self.client.register(
                    registration_endpoint, **args)
            except:
                raise LDPLoginError("cannot_register")

        session["state"] = rndstr()
        session["nonce"] = rndstr()
        args = {
            "client_id": self.client.client_id,
            "response_type": "code",
            "scope": ["openid"],
            "nonce": session["nonce"],
            "redirect_uri": self.client.registration_response["redirect_uris"][0],
            "state": session["state"]
        }

        auth_req = self.client.construct_AuthorizationRequest(request_args=args)
        return auth_req.request(self.client.authorization_endpoint)
