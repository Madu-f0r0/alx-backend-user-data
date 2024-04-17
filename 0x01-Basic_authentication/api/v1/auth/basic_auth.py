#!/usr/bin/env python3
"""This module contains the definition of the class `BasicAuth`
"""

import base64
from .auth import Auth
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """Implements the basic authentication feature
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extracts the basic authentication token from
        the Authorization header
        """
        if authorization_header is not None:
            if type(authorization_header) is str:
                if authorization_header.startswith('Basic '):
                    return authorization_header.split(' ')[-1]
        return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decodes a basic authentication token passed in the
        authorization header
        """
        if base64_authorization_header is not None:
            if type(base64_authorization_header) is str:
                try:
                    encoded = base64_authorization_header.encode('utf-8')
                    decoded = base64.b64decode(encoded)
                    return decoded.decode('utf-8')
                except Exception:
                    return None
        return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Extracts username and password from decoded authorization header
        """
        if decoded_base64_authorization_header is not None:
            if type(decoded_base64_authorization_header) is str:
                if ':' in decoded_base64_authorization_header:
                    return tuple(decoded_base64_authorization_header
                                 .split(':'))[:2]
        return None, None

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Returns a User object with the specified email and password
        if valid
        """
        if user_email is not None and type(user_email) is str:
            if user_pwd is not None and type(user_pwd) is str:
                try:
                    users = User.search({'email': user_email})
                    if users:
                        for user in users:
                            if user.is_valid_password(user_pwd):
                                return user
                except Exception:
                    return None
        return None
