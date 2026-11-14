"""Local-only launcher for the isolated synthetic dashboard UAT.

No operating API server, operating DB, broker, or provider is imported.
The password is entered interactively and never stored in this file.
"""

import getpass
import secrets

from full_dashboard_uat.app_factory import create_full_dashboard_uat_app


HOST = "127.0.0.1"
PORT = 5052


def main():
    password = getpass.getpass("Synthetic UAT password: ")

    if not password:
        raise SystemExit("UAT_PASSWORD_REQUIRED")

    session_secret = secrets.token_hex(32)

    app = create_full_dashboard_uat_app(
        password=password,
        session_secret=session_secret,
    )

    app.config.update(
        DEBUG=False,
        TESTING=False,
        PROPAGATE_EXCEPTIONS=False,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Strict",
    )

    print("SYNTHETIC_UAT_ONLY")
    print(f"LOCAL_URL=http://{HOST}:{PORT}")
    print("NO_OPERATING_DB_OR_BROKER_CALLS_AUTHORIZED")

    app.run(
        host=HOST,
        port=PORT,
        debug=False,
        use_reloader=False,
        threaded=False,
    )


if __name__ == "__main__":
    main()
