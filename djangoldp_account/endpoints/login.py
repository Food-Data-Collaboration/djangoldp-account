import validators
from django.conf import settings
from django.urls import reverse

from djangoldp_account.errors import LDPLoginError
from djangoldp_account.models import OPClient
from oic import rndstr
from oic.oic import Client
from oic.utils.authn.client import CLIENT_AUTHN_METHOD


class RPLoginEndpoint(object):
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
        redirect_uris = [settings.SITE_URL + reverse('ldp_login_callback')]
        try:
            issuer = self.client.discover(subject)
            provider_info = self.client.provider_config(issuer)
        except:
            # assume that the subject is the provider
            try:
                provider_info = self.client.provider_config(subject)
            except:
                raise LDPLoginError("cannot_get_provider_info")

        existing_op_client = OPClient.objects.filter(issuer=provider_info._dict['issuer']).first()
        if existing_op_client is None:
            try:
                registration_endpoint = provider_info._dict["registration_endpoint"]
                args = {
                    "client_name": settings.SITE_URL,
                    "response_types": ["id_token token"],
                    "redirect_uris": redirect_uris,
                }

                registration_response = self.client.register(
                    registration_endpoint, **args)

                OPClient.objects.create(issuer=provider_info._dict['issuer'],
                                client_id=self.client.client_id)
            except:
                raise LDPLoginError("cannot_register")
        else:
            self.client.client_id = existing_op_client.client_id

        self.request.session['nonce'] = rndstr()
        self.request.session['state'] = rndstr()

        args = {
            "client_id": self.client.client_id,
            "response_type": ["id_token token"],
            "scope": ["openid website"],
            "nonce": self.request.session['nonce'],
            "redirect_uri": redirect_uris[0],
            "state": self.request.session['state']
        }

        auth_req = self.client.construct_AuthorizationRequest(request_args=args)
        return auth_req.request(self.client.authorization_endpoint)
