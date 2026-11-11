"""Offline contract tests for the isolated UAT request allowlist."""

import pytest

from uat_boundary.access_policy import is_uat_request_allowed


@pytest.mark.parametrize(
    ("path", "method"),
    [
        ("/", "GET"),
        ("/static/dashboard.js", "GET"),
        ("/static/style.css", "GET"),
        ("/api/auth/login", "POST"),
        ("/api/auth/logout", "POST"),
        ("/api/auth/status", "GET"),
        ("/api/kiwoom-ver11-analysis", "POST"),
        ("/api/kiwoom-ver11-replay", "POST"),
    ],
)
def test_explicit_uat_requests_are_allowed(path, method):
    assert is_uat_request_allowed(path, method)


@pytest.mark.parametrize(
    ("path", "method"),
    [
        ("/api/auth/admin-login", "POST"),
        ("/api/auth/user-password", "POST"),
        ("/api/ver11-analysis", "GET"),
        ("/api/historical-replay", "GET"),
        ("/api/ranking", "GET"),
        ("/api/kiwoom-ver11-analysis", "GET"),
        ("/api/kiwoom-ver11-replay", "GET"),
        ("/api/auth/login", "GET"),
        ("/", "POST"),
        ("/static/dashboard.js", "POST"),
        ("/static/dashboard_step535_backup.js", "GET"),
        ("/static/dashboard_step536_backup.js", "GET"),
        ("/static/style_step535_backup.css", "GET"),
        ("/static/style_step536_backup.css", "GET"),
        ("/static/unknown.js", "GET"),
        ("/static/../config/platform_auth.json", "GET"),
        ("/static//dashboard.js", "GET"),
        ("/static/%2e%2e/config/platform_auth.json", "GET"),
        ("/static/%252e%252e/secret", "GET"),
        ("/static\\..\\config\\platform_auth.json", "GET"),
        ("/unknown", "GET"),
        ("", "GET"),
        ("api/auth/login", "POST"),
        (None, "GET"),
        ("/", None),
    ],
)
def test_unapproved_requests_fail_closed(path, method):
    assert not is_uat_request_allowed(path, method)
