from django.core.exceptions import PermissionDenied


def get_cf_connecting_ip(request):
    ip = request.META.get('HTTP_CF_CONNECTING_IP')
    if ip:
        return ip
    else:
        return "no_cf_ip"


def get_client_ip(request) -> str:
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        print("remote_addr")
        ip = request.META.get('REMOTE_ADDR')
    return ip


class FilterIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        banned_ips = []

        ip1 = get_client_ip(request)
        ip2 = get_cf_connecting_ip(request)
        print("Client IP:", ip1, "CF_IP:", ip2)
        if ip1 in banned_ips or ip2 in banned_ips:
            raise PermissionDenied

        response = self.get_response(request)
        return response
