#!/usr/bin/env python3
"""Contains the definition of the class `Auth`
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """Handles user basic authorization
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns true id a given path is not in the list of paths in
        `excluded_paths
        """
        if path is not None and excluded_paths:
            if path.endswith('/') is False:
                path += '/'
            if path in excluded_paths:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Checks if a request contains an authorization header
        and returns the specified authorization type if present
        """
        if request is not None:
            return request.headers.get('Authorization')
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Creates a user object from a login request
        """
        if self.__class__.__name__ == 'SessionAuth':
            return None
        auth_header = self.authorization_header(request)
        auth_token = self.extract_base64_authorization_header(auth_header)
        decoded_token = self.decode_base64_authorization_header(auth_token)
        user_email, user_pwd = self.extract_user_credentials(decoded_token)
        user = self.user_object_from_credentials(user_email, user_pwd)
        return user

    def session_cookie(self, request=None):
        """Returns the session cookie of a specified request
        """
        if request is not None:
            session_cookie = os.getenv('SESSION_NAME')
            return request.cookies.get(session_cookie)
        return None
