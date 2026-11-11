"""Attach the minimal UAT request allowlist to an existing Flask app.

No server startup, database initialization, credential access,
network calls, or broker operations occur in this module.
"""

from flask import abort, request

from uat_boundary.access_policy import is_uat_request_allowed


_ALLOWED_ENDPOINTS_BY_PATH = {
    "/": "home",
    "/static/dashboard.js": "static",
    "/static/style.css": "static",
    "/api/auth/login": "auth_login_api",
    "/api/auth/logout": "auth_logout_api",
    "/api/auth/status": "auth_status_api",
    "/api/kiwoom-ver11-analysis": "kiwoom_ver11_analysis_api",
    "/api/kiwoom-ver11-replay": "kiwoom_ver11_replay_api",
}

def install_uat_request_boundary(app):
    """Install the UAT guard before existing Flask request handlers."""
    if app is None:
        raise ValueError("Flask app required")

    if getattr(app, "_uat_boundary_installed", False):
        raise ValueError("UAT boundary already installed")

    def require_uat_allowlist():
        if not is_uat_request_allowed(request.path, request.method):
            abort(403)

        expected_endpoint = _ALLOWED_ENDPOINTS_BY_PATH.get(request.path)
        if request.endpoint != expected_endpoint:
            abort(403)

    app.before_request_funcs.setdefault(None, []).insert(
        0, require_uat_allowlist
    )

    app._uat_boundary_installed = True
    return app
