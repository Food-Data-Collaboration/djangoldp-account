import time
import uuid
from urllib.parse import urlparse

from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth import login, get_user_model
from django.utils.decorators import classonlymethod

from djangoldp.models import Model
from djangoldp_account.errors import LDPLoginError


class Solid(object):

    @classonlymethod
    def check_id_token_exp(cls, exp):
        """raises LDPLoginError if parameterised expiry time has passed"""
        if exp < time.time():
            raise LDPLoginError('id_token_expired')

    @classonlymethod
    def confirm_webid(cls, webid, iss):
        """
        validates that the Identity Provider (the value in the issuer claim) is authorized by the holder of the WebID
        See https://github.com/solid/webid-oidc-spec/blob/master/README.md#webid-provider-confirmation
        :param webid: the webfinger id provided
        :param iss: the issuer, identity provider
        :return: None
        :raises: LDPLoginError if unable to confirm the webid
        """
        url = urlparse(iss)
        webid_url = urlparse(webid)
        if webid_url.netloc == url.netloc:
            pass
        else:
            raise LDPLoginError('cannot_confirm_webid')
        # TODO : add the other cases

    @classonlymethod
    def get_or_create_user(cls, userinfo, webid):
        """
        retrieves an existing local copy of the user or creates one. Useful in federation- I have logged in with
        a user account from another provider to access this server
        :return: User object (of type configured by server settings)
        """
        try:
            return Model.get_or_create_external(get_user_model(), webid, username=uuid.uuid4(),
                                                first_name=userinfo.get('given_name', "Unknown"),
                                                last_name=userinfo.get('family_name', "Unknown"),
                                                email=userinfo.get('email', ''),)
        except ObjectDoesNotExist:
            raise Http404()
