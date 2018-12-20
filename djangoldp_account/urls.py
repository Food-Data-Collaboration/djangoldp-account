"""djangoldp project URL Configuration"""
from django.conf.urls import url
from djangoldp.views import LDPViewSet

from .models import ChatProfile, Account, ChatConfig

urlpatterns = [
    url(r'^accounts/', LDPViewSet.urls(model=Account)),
    url(r'^chat-profile/', LDPViewSet.urls(model=ChatProfile)),
    url(r'^chat-config/', LDPViewSet.urls(model=ChatConfig)),
]
