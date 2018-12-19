"""djangoldp project URL Configuration"""
from django.conf.urls import url
from djangoldp.views import LDPViewSet

from .models import ChatProfile, Account

urlpatterns = [
    url(r'^accounts/', LDPViewSet.urls(model=Account)),
    url(r'^chat-profile/', LDPViewSet.urls(model=ChatProfile)),
]
