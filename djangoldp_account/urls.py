"""djangoldp project URL Configuration"""
from importlib import import_module

from django.conf import settings
from django.conf.urls import url, include
from django.contrib.auth.models import Group
from djangoldp.views import LDPViewSet

from .models import ChatProfile, Account
from .views import userinfocustom

djangoldp_modules = list(filter(lambda app: app.startswith('djangoldp_'), settings.INSTALLED_APPS))
user_fields = ['@id', 'first_name', 'groups', 'last_name', 'username', 'email', 'profile', 'account',
               'ldnotification_set', 'chatProfile']
user_nested_fields = ['account', 'profile', 'groups', 'ldnotification_set', 'chatProfile']
for dldp_module in djangoldp_modules:
    try:
        user_fields += import_module(dldp_module + '.settings').USER_NESTED_FIELDS
        user_nested_fields += import_module(dldp_module + '.settings').USER_NESTED_FIELDS
    except:
        pass

urlpatterns = [
    url(r'^groups/', LDPViewSet.urls(model=Group, fields=['@id', 'name', 'user_set'])),
    url(r'^users/', LDPViewSet.urls(model=settings.AUTH_USER_MODEL, fields=user_fields, permission_classes=[],
                                    nested_fields=user_nested_fields)),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/', LDPViewSet.urls(model=Account)),
    url(r'^chat-profile/', LDPViewSet.urls(model=ChatProfile)),
    url(r'^openid/userinfo', userinfocustom),
    url(r'^openid/', include('oidc_provider.urls', namespace='oidc_provider')),
]
