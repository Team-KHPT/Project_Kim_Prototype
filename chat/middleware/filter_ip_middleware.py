from django.core.exceptions import PermissionDenied


def get_cf_connecting_ip(request):
    ip = request.META.get('HTTP_CF_CONNECTING_IP')
    if ip:
        return ip
    else:
        return "no_cf_ip"


def get_x_forwarded_for(request) -> str:
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for
    else:
        return "no_xff"


def get_x_real_ip(request) -> str:
    x_real_ip = request.META.get("HTTP_X_REAL_IP")
    if x_real_ip:
        return x_real_ip
    else:
        return "no_real_ip"


class FilterIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        banned_ips = []

        ip1 = get_x_forwarded_for(request)
        ip2 = get_cf_connecting_ip(request)
        ip3 = get_x_real_ip(request)
        print(f"xf:{ip1} cf:{ip2} rl:{ip3}")
        if ip1.split(",")[0] in banned_ips:
            raise PermissionDenied
        if ip2 in banned_ips or ip3 in banned_ips:
            raise PermissionDenied

        response = self.get_response(request)
        return response
