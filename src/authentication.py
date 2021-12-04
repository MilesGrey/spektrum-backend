from functools import wraps

from firebase_admin import auth
from flask import request, abort


def require_token(check_user=False):
    def require_token_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                id_token = request.headers['Authorization'][7:]
                decoded_token = auth.verify_id_token(id_token)

                if check_user:
                    if decoded_token['email'] != kwargs['user_id']:
                        raise ValueError

                return f(*args, **kwargs)
            except Exception:
                return abort(403, 'Authentication failed.')
        return wrapper
    return require_token_decorator
