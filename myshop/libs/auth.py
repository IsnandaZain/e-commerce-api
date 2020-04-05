from functools import wraps

from flask import g, request
from werkzeug.local import LocalProxy

from myshop.exceptions import BadRequest, Forbidden
from configuration import MyShopConfig

# object user ter-authentifikasi
user = LocalProxy(lambda: getattr(g, 'user_auth', None))

def internal():
    """Decorator to protect usign in internal only"""

    def decorator(f):
        @wraps(f)
        def decorator_function(*args, **kwargs):
            _auth_internal()
            return f(*args, **kwargs)

        return decorator_function


def _auth():
    if not user:
        raise BadRequest("Missing auth header")


def _auth_internal():
    token = request.headers.get("auth")
    if not token:
        raise BadRequest("Missing auth header")

    if token != MyShopConfig.INTERNAL_TOKEN:
        raise BadRequest("Wrong token")