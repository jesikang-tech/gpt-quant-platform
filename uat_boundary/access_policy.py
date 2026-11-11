"""Minimal allowlist for isolated KIWOOM Ver1.1 browser UAT.

Pure request policy only. No Flask startup, database access,
authentication changes, network calls, or broker operations.
"""

from urllib.parse import unquote


_ALLOWED_API_METHODS = {
    "/api/auth/login": frozenset({"POST"}),
    "/api/auth/logout": frozenset({"POST"}),
    "/api/auth/status": frozenset({"GET"}),
    "/api/kiwoom-ver11-analysis": frozenset({"POST"}),
    "/api/kiwoom-ver11-replay": frozenset({"POST"}),
}


def is_uat_request_allowed(path: str, method: str) -> bool:
    """Fail closed for all routes outside the explicit UAT scope."""
    if type(path) is not str or type(method) is not str:
        return False

    if not path.startswith("/") or "\\" in path:
        return False

    if "%" in path:
        return False

    if unquote(path) != path:
        return False

    if method == "GET" and path == "/":
        return True

    if method == "GET" and path in (
        "/static/dashboard.js",
        "/static/style.css",
    ):
        return True

    return method in _ALLOWED_API_METHODS.get(path, ())
