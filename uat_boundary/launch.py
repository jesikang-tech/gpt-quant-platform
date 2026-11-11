"""Explicit loopback-only launcher for isolated KIWOOM Ver1.1 UAT.

No server starts on import. This module does not import the operating
API server or load operating database and broker credentials.
"""

import os

from uat_boundary.app_factory import create_uat_app


def build_launch_app(*, password, session_secret):
    """Reuse the verified UAT app factory without starting a server."""
    return create_uat_app(
        password=password,
        session_secret=session_secret,
    )


def main():
    """Start only the isolated UAT app with explicit test credentials."""
    password = os.environ.get("KIWOOM_UAT_PASSWORD")
    session_secret = os.environ.get("KIWOOM_UAT_SESSION_SECRET")

    if not password:
        raise RuntimeError("Explicit UAT password required")

    if not session_secret or len(session_secret) < 32:
        raise RuntimeError("Strong UAT session secret required")

    app = build_launch_app(
        password=password,
        session_secret=session_secret,
    )

    app.run(
        host="127.0.0.1",
        port=5051,
        debug=False,
        use_reloader=False,
        threaded=False,
    )


if __name__ == "__main__":
    main()