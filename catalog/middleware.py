import threading
from typing import Optional
from django.utils.deprecation import MiddlewareMixin

_user_local = threading.local()

def set_current_user(user):
    _user_local.user = user

def get_current_user() -> Optional[object]:
    return getattr(_user_local, 'user', None)

class CurrentUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        set_current_user(getattr(request, 'user', None))
        return None
    def process_response(self, request, response):
        set_current_user(None)
        return response
