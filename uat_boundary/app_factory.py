"""Construct an isolated KIWOOM Ver1.1 UAT Flask app.

This module does not import api_server, initialize a database,
load operating credentials, start a server, or call a broker.

The factory is intentionally incomplete until isolated authentication
and offline API routes are registered and tested.
"""

from pathlib import Path

from flask import Flask

from uat_boundary.browser_boundary import render_uat_dashboard
from uat_boundary.flask_boundary import install_uat_request_boundary
from uat_boundary.kiwoom_routes import register_kiwoom_uat_routes
from uat_boundary.uat_auth import register_uat_auth


_PROJECT_ROOT = Path(__file__).resolve().parent.parent


def create_uat_app(*, password, session_secret):
    """Build a non-operational UAT app with isolated authentication."""
    if type(password) is not str or not password:
        raise ValueError("Explicit UAT password required")
    if type(session_secret) is not str or len(session_secret) < 32:
        raise ValueError("Strong UAT session secret required")
    app = Flask(
        "kiwoom_ver11_isolated_uat",
        template_folder=str(_PROJECT_ROOT / "templates"),
        static_folder=str(_PROJECT_ROOT / "static"),
        static_url_path="/static",
    )

    app.config.update(
        TESTING=False,
        DEBUG=False,
        PROPAGATE_EXCEPTIONS=False,
    )

    @app.route("/")
    def home():
        return render_uat_dashboard()

    app.secret_key = session_secret

    register_uat_auth(app, password=password)
    register_kiwoom_uat_routes(app)
    install_uat_request_boundary(app)

    return app
