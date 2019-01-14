"""djangoldp project URL Configuration"""
from django.conf.urls import url, include
from djangoldp.views import LDPViewSet

from .models import ChatProfile, Account, ChatConfig
from .views import userinfocustom

urlpatterns = [
    url(r'^accounts/', LDPViewSet.urls(model=Account)),
    url(r'^chat-profile/', LDPViewSet.urls(model=ChatProfile)),
    url(r'^chat-config/', LDPViewSet.urls(model=ChatConfig)),
    url(r'^openid/userinfo', userinfocustom),
    url(r'^openid/', include('oidc_provider.urls', namespace='oidc_provider')),
]
