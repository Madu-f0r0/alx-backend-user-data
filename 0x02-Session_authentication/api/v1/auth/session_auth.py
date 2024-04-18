#!/usr/bin/env python3
"""Contains the definition of the class SessionAuth
"""

from .auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """Implements session authentication
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session id for a user
        """
        if user_id is not None and type(user_id) is str:
            session_id = str(uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id
        return None

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns the user id for a specified session id
        """
        if session_id is not None and type(session_id) is str:
            return self.user_id_by_session_id.get(session_id)
        return None

    def current_user(self, request=None):
        """Returns the current user sending a specified request
        using the session cookie in the request header
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """Deletes a user session (logout functionality)
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if user_id is not None:
            self.user_id_by_session_id.pop(session_id)
            return True
        return False
