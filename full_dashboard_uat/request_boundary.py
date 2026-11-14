"""Fail-closed request allowlist for the synthetic full-dashboard UAT.

Only explicitly registered route/method/endpoint combinations are
permitted. This is a Flask request boundary, not an OS sandbox.
"""

from flask import abort, request


_BASE_ROUTES = {
    ("/", "GET"): "home",
    ("/static/dashboard.js", "GET"): "static",
    ("/static/style.css", "GET"): "static",
    ("/uat-assets/chart.umd.js", "GET"): "uat_chart_asset",
    ("/api/auth/login", "POST"): "auth_login_api",
    ("/api/auth/logout", "POST"): "auth_logout_api",
    ("/api/auth/status", "GET"): "auth_status_api",
}


def install_full_dashboard_request_boundary(app, *, synthetic_routes=None):
    """Install an exact-match allowlist ahead of authentication hooks."""
    if app is None:
        raise ValueError("Flask app required")

    if getattr(app, "_full_dashboard_boundary_installed", False):
        raise ValueError("Full-dashboard UAT boundary already installed")

    routes = dict(_BASE_ROUTES)

    if synthetic_routes is not None:
        if type(synthetic_routes) is not dict:
            raise ValueError("Synthetic routes must be an explicit dict")

        for key, endpoint in synthetic_routes.items():
            if (
                type(key) is not tuple
                or len(key) != 2
                or type(key[0]) is not str
                or type(key[1]) is not str
                or type(endpoint) is not str
                or not endpoint
            ):
                raise ValueError("Invalid synthetic route declaration")

            path, method = key

            if (
                not path.startswith("/api/")
                or path.startswith("/api/auth/")
                or method not in {"GET", "POST"}
                or key in routes
            ):
                raise ValueError("Forbidden synthetic route declaration")

            routes[key] = endpoint

    def require_full_dashboard_allowlist():
        key = (request.path, request.method)
        expected_endpoint = routes.get(key)

        if (
            expected_endpoint is None
            and request.method == "GET"
            and request.path.startswith("/api/ver11-analysis/snapshots/")
            and request.endpoint == "synthetic_ver11_snapshot_detail_api"
        ):
            snapshot_id = request.path.rsplit("/", 1)[-1]
            if (
                snapshot_id.isascii()
                and snapshot_id.isdecimal()
                and len(snapshot_id) <= 12
                and snapshot_id != "0"
            ):
                expected_endpoint = "synthetic_ver11_snapshot_detail_api"

        if expected_endpoint is None:
            abort(403)

        if request.endpoint != expected_endpoint:
            abort(403)

    app.before_request_funcs.setdefault(None, []).insert(
        0,
        require_full_dashboard_allowlist,
    )

    app._full_dashboard_boundary_installed = True
    return app
