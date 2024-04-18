#!/usr/bin/env python3
"""Contains the definition of the class SessionAuth
"""

from .auth import Auth
from uuid import uuid4


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
