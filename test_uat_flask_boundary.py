"""Isolated Flask request-boundary tests without importing api_server."""

import pytest
from flask import Flask

from uat_boundary.flask_boundary import install_uat_request_boundary


def make_app():
    app = Flask(__name__)

    @app.before_request
    def existing_authentication_check():
        return "EXISTING_AUTH", 401

    @app.route("/")
    def home():
        return "HOME"

    @app.route("/api/auth/login", methods=["POST"])
    def auth_login_api():
        return "LOGIN"

    @app.route("/api/auth/logout", methods=["POST"])
    def auth_logout_api():
        return "LOGOUT"

    @app.route("/api/auth/status")
    def auth_status_api():
        return "STATUS"

    @app.route("/api/kiwoom-ver11-analysis", methods=["POST"])
    def kiwoom_ver11_analysis_api():
        return "ANALYSIS"

    @app.route("/api/kiwoom-ver11-replay", methods=["POST"])
    def kiwoom_ver11_replay_api():
        return "REPLAY"

    @app.route("/api/auth/admin-login", methods=["POST"])
    def auth_admin_login_api():
        return "ADMIN"

    @app.route("/api/ranking")
    def ranking_api():
        return "RANKING"

    install_uat_request_boundary(app)
    return app


@pytest.mark.parametrize(
    ("path", "method"),
    [
        ("/", "GET"),
        ("/api/auth/login", "POST"),
        ("/api/auth/logout", "POST"),
        ("/api/auth/status", "GET"),
        ("/api/kiwoom-ver11-analysis", "POST"),
        ("/api/kiwoom-ver11-replay", "POST"),
    ],
)
def test_allowed_requests_reach_existing_authentication(path, method):
    client = make_app().test_client()
    response = client.open(path, method=method)
    assert response.status_code == 401
    assert response.get_data(as_text=True) == "EXISTING_AUTH"


@pytest.mark.parametrize(
    ("path", "method"),
    [
        ("/api/auth/admin-login", "POST"),
        ("/api/ranking", "GET"),
        ("/api/kiwoom-ver11-analysis", "GET"),
        ("/api/auth/login", "GET"),
        ("/unknown", "GET"),
    ],
)
def test_disallowed_requests_stop_before_existing_authentication(path, method):
    client = make_app().test_client()
    response = client.open(path, method=method)
    assert response.status_code == 403


def test_duplicate_boundary_installation_fails_closed():
    app = make_app()
    with pytest.raises(ValueError, match="already installed"):
        install_uat_request_boundary(app)


def test_missing_app_is_rejected():
    with pytest.raises(ValueError, match="Flask app required"):
        install_uat_request_boundary(None)


def test_wrong_endpoint_name_is_rejected():
    app = Flask(__name__)

    @app.route("/")
    def wrong_home_endpoint():
        return "WRONG"

    install_uat_request_boundary(app)
    response = app.test_client().get("/")
    assert response.status_code == 403


def test_allowed_path_with_wrong_api_endpoint_is_rejected():
    app = Flask(__name__)

    @app.route("/api/kiwoom-ver11-analysis", methods=["POST"])
    def wrong_analysis_endpoint():
        return "WRONG"

    install_uat_request_boundary(app)
    response = app.test_client().post("/api/kiwoom-ver11-analysis")
    assert response.status_code == 403


def test_allowed_static_path_with_wrong_endpoint_is_rejected():
    app = Flask(__name__, static_folder=None)

    @app.route("/static/dashboard.js")
    def wrong_static_endpoint():
        return "WRONG"

    install_uat_request_boundary(app)
    response = app.test_client().get("/static/dashboard.js")
    assert response.status_code == 403
