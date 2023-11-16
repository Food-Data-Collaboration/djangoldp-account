from django.conf import settings
from rest_framework.filters import BaseFilterBackend

XMPP_SERVERS = set({'51.15.243.248', '212.47.234.179', '2001:bc8:47b0:2711::1'})

if hasattr(settings, 'XMPP_SERVER_IP'):
    XMPP_SERVERS = XMPP_SERVERS.union(getattr(settings, 'XMPP_SERVER_IP'))

def check_client_ip(request):
    x_forwarded_for = request.headers.get('x-forwarded-for')
    if x_forwarded_for:
        ip = x_forwarded_for.replace(' ', '').split(',')
    else:
        ip = request.META.get('REMOTE_ADDR')

    if isinstance(ip, list):
        if any(i in ip for i in XMPP_SERVERS):
            return True
    elif ip in XMPP_SERVERS:
        return True

    return False

class IPFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if check_client_ip(request):
            return queryset
        else:
            return queryset.none()