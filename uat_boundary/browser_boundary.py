"""Browser resource boundary for isolated KIWOOM Ver1.1 UAT.

Does not modify the operating dashboard template or static assets.
This is browser-side defense, not an OS-level network or DB sandbox.
"""

from flask import make_response, render_template


_CHART_CDN_TAG = (
    '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>'
)

_UAT_CSP = "; ".join((
    "default-src 'none'",
    "script-src 'self' 'unsafe-inline'",
    "style-src 'self'",
    "img-src 'self' data:",
    "font-src 'self'",
    "connect-src 'self'",
    "object-src 'none'",
    "frame-src 'none'",
    "frame-ancestors 'none'",
    "base-uri 'none'",
    "form-action 'self'",
))


def render_uat_dashboard():
    """Render the existing template without its external Chart.js CDN."""
    html = render_template("index.html")

    if html.count(_CHART_CDN_TAG) != 1:
        raise RuntimeError("Unexpected dashboard CDN contract")

    html = html.replace(_CHART_CDN_TAG, "")

    response = make_response(html)
    response.headers["Content-Security-Policy"] = _UAT_CSP
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cache-Control"] = "no-store"

    return response
