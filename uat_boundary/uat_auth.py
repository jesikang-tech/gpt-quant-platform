"""Memory-only authentication for isolated KIWOOM Ver1.1 UAT.

Does not read or modify operating authentication configuration.
Credentials are supplied explicitly by the UAT app factory.
"""

import hmac

from flask import jsonify, request, session


def register_uat_auth(app, *, password):
    """Register UAT-only login, logout, status and session protection."""
    if not isinstance(password, str) or not password:
        raise ValueError("Explicit UAT password required")

    if not app.secret_key:
        raise ValueError("UAT session secret must be configured first")

    if getattr(app, "_uat_auth_registered", False):
        raise ValueError("UAT authentication already registered")

    @app.before_request
    def require_uat_authentication():
        if request.endpoint in {
            "home",
            "static",
            "auth_login_api",
            "auth_status_api",
        }:
            return None

        if (
            request.path.startswith("/api/")
            and session.get("authenticated") is not True
        ):
            return jsonify({"success": False}), 401

        return None

    @app.route("/api/auth/login", methods=["POST"])
    def auth_login_api():
        body = request.get_json(silent=True)
        if type(body) is not dict:
            return jsonify({"success": False}), 401

        supplied = body.get("password")
        if type(supplied) is not str:
            return jsonify({"success": False}), 401

        if not hmac.compare_digest(supplied, password):
            return jsonify({"success": False}), 401

        session.clear()
        session["authenticated"] = True
        session["role"] = "user"
        return jsonify({"success": True})

    @app.route("/api/auth/logout", methods=["POST"])
    def auth_logout_api():
        session.clear()
        return jsonify({"success": True})

    @app.route("/api/auth/status", methods=["GET"])
    def auth_status_api():
        return jsonify({
            "authenticated": session.get("authenticated", False),
            "role": session.get("role"),
        })

    app._uat_auth_registered = True
    return app
