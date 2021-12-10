from functools import wraps

from firebase_admin import auth
from firebase_admin.auth import UserDisabledError, CertificateFetchError, RevokedIdTokenError, InvalidIdTokenError
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
            except (ValueError, InvalidIdTokenError, RevokedIdTokenError, CertificateFetchError, UserDisabledError)\
                    as e:
                return abort(403, 'Authentication failed.')
            return f(*args, **kwargs)

        return wrapper
    return require_token_decorator


def authenticate_user(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token['email']
    except (ValueError, InvalidIdTokenError, RevokedIdTokenError, CertificateFetchError, UserDisabledError) as e:
        raise AuthenticationError(e.message)


class AuthenticationError(Exception):
    """Raised when authentication fails."""
    pass

