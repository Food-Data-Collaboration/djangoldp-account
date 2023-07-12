"""djangoldp project URL Configuration"""

from pydoc import locate
from django.conf import settings
from django.urls import path, re_path, include
from django.contrib.auth.models import Group
from django.views.decorators.csrf import csrf_exempt

from djangoldp.permissions import LDPPermissions
from djangoldp.views import LDPViewSet
from djangoldp_account.forms import LDPUserForm
from .models import ChatProfile, Account
from .views import userinfocustom, RPLoginView, RPLoginCallBackView, check_user, LDPAccountLoginView, RedirectView, \
    LDPAccountRegistrationView

Group._meta.serializer_fields = ['name']
Group._meta.anonymous_perms = getattr(settings, 'GROUP_ANONYMOUS_PERMISSIONS', ['view'])
Group._meta.authenticated_perms = getattr(settings, 'GROUP_AUTHENTICATED_PERMISSIONS', ['inherit'])
Group._meta.owner_perms = getattr(settings, 'GROUP_OWNER_PERMISSIONS', ['inherit'])

user_form_override = getattr(settings, 'REGISTRATION_USER_FORM', None)
user_form = LDPUserForm if user_form_override is None else locate(user_form_override)

urlpatterns = [
    path('groups/',
        LDPViewSet.urls(model=Group, fields=['@id', 'name', 'user_set'],
                        permission_classes=getattr(settings, 'GROUP_PERMISSION_CLASSES', [LDPPermissions]),
        )
    ),
    path('auth/register/',
        LDPAccountRegistrationView.as_view(
            form_class=user_form
        ),
        name='django_registration_register',
    ),
    path('auth/login/', LDPAccountLoginView.as_view(),name='login'),
    path('auth/', include('django_registration.backends.activation.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('accounts/', LDPViewSet.urls(model=Account, permission_classes=[LDPPermissions], model_prefix='pk_lookup',
                                       lookup_field='pk')),
    path('chat-profile/', LDPViewSet.urls(model=ChatProfile, permission_classes=[LDPPermissions],
                                           model_prefix='pk_lookup', lookup_field='pk')),
    re_path(r'^oidc/login/callback/?$', RPLoginCallBackView.as_view(), name='oidc_login_callback'),
    re_path(r'^oidc/login/?$', RPLoginView.as_view(), name='oidc_login'),
    re_path(r'^userinfo/?$', csrf_exempt(userinfocustom)),
    re_path(r'^check-user/?$', csrf_exempt(check_user)),
    path('redirect-default/', RedirectView.as_view(),name='redirect-default'),
    path('', include('oidc_provider.urls', namespace='oidc_provider'))
]
