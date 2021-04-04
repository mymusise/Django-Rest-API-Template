from django.utils.deprecation import MiddlewareMixin
from .logger import request_logger


class APILogMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    @classmethod
    def log_request(cls, request):
        # TODO: mask security params such like `password` or `token`
        user = getattr(request, "user")
        method = str(getattr(request, "method", "")).upper()
        request_path = str(getattr(request, "path", ""))
        query = dict(getattr(request, method, {}))
        try:
            data = getattr(request, "data", "{}")
        except Exception as e:
            request_logger.error(e)
            data = {}
        request_logger.info(
            {
                "method": method,
                "path": request_path,
                "user.username": user.username if user else "",
                "user.id": user.id if user else None,
                "query": query,
                "data": data,
            }
        )

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.id is None:
            pass
        else:
            self.log_request(request)
