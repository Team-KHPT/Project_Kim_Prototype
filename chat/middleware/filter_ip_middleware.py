from django.core.exceptions import PermissionDenied


class FilterIPMiddleware(object):
    def process_request(self, request):
        banned_ips = []

        print(request.META.get('HTTP_X_FORWARDED_FOR'), request.META.get('HTTP_CF_CONNECTING_IP'))
        ip = request.META.get('HTTP_CF_CONNECTING_IP')
        if ip in banned_ips:
            raise PermissionDenied

        return None
