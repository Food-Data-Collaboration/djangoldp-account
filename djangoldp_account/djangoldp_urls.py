"""djangoldp project URL Configuration"""
from importlib import import_module

from django.conf import settings
from django.conf.urls import url, include
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.views.decorators.csrf import csrf_exempt

from djangoldp.permissions import LDPPermissions
from djangoldp.views import LDPViewSet
from .models import ChatProfile, Account
from .views import userinfocustom, RPLoginView, RPLoginCallBackView, check_user

user_model = get_user_model()
djangoldp_modules = list(settings.DJANGOLDP_PACKAGES)
user_fields = ['@id', 'first_name', 'groups', 'last_name', 'username', 'email', 'account', 'chatProfile', 'name']
user_nested_fields = ['account', 'groups', 'chatProfile']
for dldp_module in djangoldp_modules:
    try:
        module_user_nested_fields = import_module(dldp_module + '.settings').USER_NESTED_FIELDS
        user_fields += module_user_nested_fields
        user_nested_fields += module_user_nested_fields
    except:
        pass

urlpatterns = [
    url(r'^groups/',
        LDPViewSet.urls(model=Group, fields=['@id', 'name', 'user_set'],
                        permission_classes=getattr(settings, 'GROUP_PERMISSION_CLASSES', [LDPPermissions]),
                        )),
    url(r'^users/',
        LDPViewSet.urls(model=settings.AUTH_USER_MODEL, fields=user_fields,
                        permission_classes=getattr(settings, 'USER_PERMISSION_CLASSES', [LDPPermissions]),
                        nested_fields=user_nested_fields
                        )),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/', LDPViewSet.urls(model=Account, permission_classes=[LDPPermissions])),
    url(r'^chat-profile/', LDPViewSet.urls(model=ChatProfile, permission_classes=[LDPPermissions])),
    url(r'^oidc/login/callback/?$', RPLoginCallBackView.as_view(), name='oidc_login_callback'),
    url(r'^oidc/login/?$', RPLoginView.as_view(), name='oidc_login'),
    url(r'^userinfo/?$', csrf_exempt(userinfocustom)),
    url(r'^check-user/?$', csrf_exempt(check_user)),
    url(r'^', include('oidc_provider.urls', namespace='oidc_provider'))
]
s_fields = []
s_fields.extend(user_fields)
s_fields.extend(user_nested_fields)
user_model._meta.serializer_fields = s_fields
user_model._meta.anonymous_perms = getattr(settings, 'USER_ANONYMOUS_PERMISSIONS', ['view'])
user_model._meta.authenticated_perms = getattr(settings, 'USER_AUTHENTICATED_PERMISSIONS', ['inherit'])
user_model._meta.owner_perms = getattr(settings, 'USER_OWNER_PERMISSIONS', ['inherit'])
Group._meta.serializer_fields = ['name']
Group._meta.anonymous_perms = getattr(settings, 'GROUP_ANONYMOUS_PERMISSIONS', ['view'])
Group._meta.authenticated_perms = getattr(settings, 'GROUP_AUTHENTICATED_PERMISSIONS', ['inherit']),
Group._meta.owner_perms = getattr(settings, 'GROUP_OWNER_PERMISSIONS', ['inherit']),
