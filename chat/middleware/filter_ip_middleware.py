from django.core.exceptions import PermissionDenied


class FilterIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # 최초 설정 및 초기화

    def __call__(self, request):
        banned_ips = []

        print(request.META.get('HTTP_X_FORWARDED_FOR'), request.META.get('HTTP_CF_CONNECTING_IP'))
        ip = request.META.get('HTTP_CF_CONNECTING_IP')
        if ip in banned_ips:
            raise PermissionDenied

        response = self.get_response(request)

        return response
