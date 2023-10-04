from rest_framework.filters import BaseFilterBackend
from djangoldp_circle.xmpp import get_client_ip, XMPP_SERVERS

class IPFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if get_client_ip(request) in XMPP_SERVERS:
            return queryset
        else:
            return queryset.none()