from django.shortcuts import redirect
import ipaddress
from django.contrib import messages as popup_messages


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_REMOTE_ADDR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def filter_ip_middleware(get_response):
    def middleware(request):
        ip = get_client_ip(request)
        if request.path.startswith('/admin/'):
            if not (ipaddress.ip_address(ip) in ipaddress.ip_network('147.175.0.0/16')):
                popup_messages.error(request,'Na prístup do administrátorskej časti musíte byť pripojený na sieť STU.')
                return redirect('cars')
        response = get_response(request)
        return response
    return middleware
