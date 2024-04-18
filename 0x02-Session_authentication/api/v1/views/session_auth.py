#!/usr/bin/env python3
"""Handles all routes for session authentication
"""

import os
from flask import jsonify, request
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session_login():
    """
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': email})

    for user in users:
        if not user:
            return jsonify({"error": "no user found for this email"}), 404
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)

            response = jsonify(user.to_json())
            response.set_cookie(os.getenv('SESSION_NAME'), session_id)

            return response
    return jsonify({"error": "wrong password"}), 401
