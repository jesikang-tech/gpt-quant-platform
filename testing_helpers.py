"""Shared helpers for authenticated Flask API contract tests."""


def authenticated_client(app):
    app.secret_key = "test-auth-session-secret-key"
    client = app.test_client()
    with client.session_transaction() as flask_session:
        flask_session["authenticated"] = True
        flask_session["role"] = "user"
    return client