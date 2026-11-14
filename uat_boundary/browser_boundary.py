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
    "style-src-attr 'unsafe-inline'",
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

    html = html.replace(
        _CHART_CDN_TAG,
        '<script src="/uat-assets/chart.umd.js"></script>',
        1,
    )

    # Adapt only the isolated UAT HTML response.
    login_input = 'id="platform-auth-password"'
    if html.count(login_input) != 1:
        raise RuntimeError("Unexpected UAT login input contract")

    html = html.replace(
        login_input,
        'id="platform-auth-password" data-uat-login="true"',
        1,
    )

    dashboard_tag = '<script src="/static/dashboard.js"></script>'
    if html.count(dashboard_tag) != 1:
        raise RuntimeError("Unexpected dashboard script contract")

    uat_script = """
<script>
document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("platform-auth-password");
    const adminToggle = document.getElementById("platform-admin-toggle");

    if (!input || !adminToggle) {
        return;
    }

    function applyUatPasswordInput() {
        input.removeAttribute("maxlength");
        input.removeAttribute("pattern");
        input.setAttribute("inputmode", "text");
        input.setAttribute("aria-label", "UAT password");
    }

    adminToggle.hidden = true;
    adminToggle.disabled = true;

    if (typeof setPlatformAuthMode === "function") {
        const originalSetPlatformAuthMode = setPlatformAuthMode;

        setPlatformAuthMode = function () {
            originalSetPlatformAuthMode("user");
            applyUatPasswordInput();
        };
    }

    if (typeof isValidPlatformPassword === "function") {
        isValidPlatformPassword = function (password) {
            return typeof password === "string" && password.length > 0;
        };
    }

    applyUatPasswordInput();
});
</script>
"""

    html = html.replace(
        dashboard_tag,
        dashboard_tag + uat_script,
        1,
    )

    response = make_response(html)
    response.headers["Content-Security-Policy"] = _UAT_CSP
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cache-Control"] = "no-store"

    return response
