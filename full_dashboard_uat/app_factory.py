"""Construct a separate synthetic full-dashboard UAT Flask application.

Do not import the operating api_server, initialize databases,
load operating credentials, or perform broker requests.

This factory is not ready for server execution until a separate
fail-closed request boundary and synthetic API routes are installed.
"""

from pathlib import Path

from flask import Flask, send_file

from uat_boundary.browser_boundary import render_uat_dashboard
from uat_boundary.uat_auth import register_uat_auth
from full_dashboard_uat.request_boundary import install_full_dashboard_request_boundary
from full_dashboard_uat.synthetic_ranking import register_synthetic_ranking
from full_dashboard_uat.synthetic_intelligence import register_synthetic_intelligence
from full_dashboard_uat.synthetic_etf_detail import register_synthetic_etf_detail
from full_dashboard_uat.synthetic_portfolio import register_synthetic_portfolio
from full_dashboard_uat.synthetic_portfolio_views import register_synthetic_portfolio_views
from full_dashboard_uat.synthetic_market_views import register_synthetic_market_views
from full_dashboard_uat.synthetic_ai_core import register_synthetic_ai_core
from full_dashboard_uat.synthetic_ai_extensions import register_synthetic_ai_extensions
from full_dashboard_uat.synthetic_complex_views import register_synthetic_complex_views
from full_dashboard_uat.synthetic_ver11_snapshots import register_synthetic_ver11_snapshots
from uat_boundary.kiwoom_routes import register_kiwoom_uat_routes


_PROJECT_ROOT = Path(__file__).resolve().parent.parent


def create_full_dashboard_uat_app(*, password, session_secret):
    """Build the isolated application without operating API routes."""
    if type(password) is not str or not password:
        raise ValueError("Explicit UAT password required")

    if type(session_secret) is not str or len(session_secret) < 32:
        raise ValueError("Strong UAT session secret required")

    app = Flask(
        "full_dashboard_synthetic_uat",
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

    @app.route("/uat-assets/chart.umd.js", methods=["GET"])
    def uat_chart_asset():
        return send_file(
            _PROJECT_ROOT / "full_dashboard_uat" / "vendor" / "chart.umd.js",
            mimetype="application/javascript",
        )

    app.secret_key = session_secret

    register_uat_auth(app, password=password)

    synthetic_routes = register_synthetic_ranking(app)
    synthetic_routes.update(register_synthetic_intelligence(app))
    synthetic_routes.update(register_synthetic_etf_detail(app))
    synthetic_routes.update(register_synthetic_portfolio(app))
    synthetic_routes.update(register_synthetic_portfolio_views(app))
    synthetic_routes.update(register_synthetic_market_views(app))
    synthetic_routes.update(register_synthetic_ai_core(app))
    synthetic_routes.update(register_synthetic_ai_extensions(app))
    synthetic_routes.update(register_synthetic_complex_views(app))
    synthetic_routes.update(register_synthetic_ver11_snapshots(app))
    register_kiwoom_uat_routes(app)
    synthetic_routes.update({
        ("/api/kiwoom-ver11-analysis", "POST"):
            "kiwoom_ver11_analysis_api",
        ("/api/kiwoom-ver11-replay", "POST"):
            "kiwoom_ver11_replay_api",
    })

    install_full_dashboard_request_boundary(
        app,
        synthetic_routes=synthetic_routes,
    )

    return app
