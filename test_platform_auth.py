from core.platform_auth import validate_password_format


def test_user_password_requires_exactly_four_ascii_digits():
    assert validate_password_format("1234") is True
    assert validate_password_format("123") is False
    assert validate_password_format("12345") is False
    assert validate_password_format("12A4") is False
    assert validate_password_format("\uFF11\uFF12\uFF13\uFF14") is False


def test_admin_password_requires_exactly_seven_ascii_digits():
    assert validate_password_format("1234567", admin=True) is True
    assert validate_password_format("123456", admin=True) is False
    assert validate_password_format("12345678", admin=True) is False
    assert validate_password_format("123A567", admin=True) is False
    assert validate_password_format("\uFF11\uFF12\uFF13\uFF14\uFF15\uFF16\uFF17", admin=True) is False

def test_user_password_hash_is_not_plaintext_and_verifies_correctly():
    from core.platform_auth import create_password_hash, verify_password

    password_hash = create_password_hash("1234")

    assert password_hash != "1234"
    assert verify_password(password_hash, "1234") is True
    assert verify_password(password_hash, "9999") is False


def test_admin_password_hash_is_not_plaintext_and_verifies_correctly():
    from core.platform_auth import create_password_hash, verify_password

    password_hash = create_password_hash("1234567", admin=True)

    assert password_hash != "1234567"
    assert verify_password(password_hash, "1234567", admin=True) is True
    assert verify_password(password_hash, "7654321", admin=True) is False

def test_invalid_password_formats_cannot_be_hashed():
    import pytest
    from core.platform_auth import create_password_hash

    with pytest.raises(ValueError):
        create_password_hash("123")

    with pytest.raises(ValueError):
        create_password_hash("12A4")

    with pytest.raises(ValueError):
        create_password_hash("123456", admin=True)

    with pytest.raises(ValueError):
        create_password_hash("123A567", admin=True)

def test_auth_config_persists_only_password_hashes(tmp_path):
    import json

    from core.platform_auth import create_password_hash, save_auth_config

    config_path = tmp_path / "platform_auth.json"
    user_hash = create_password_hash("1234")
    admin_hash = create_password_hash("1234567", admin=True)

    save_auth_config(user_hash, admin_hash, config_path)

    data = json.loads(config_path.read_text(encoding="utf-8"))

    assert data["user_password_hash"] == user_hash
    assert data["admin_password_hash"] == admin_hash
    assert "1234" not in data.values()
    assert "1234567" not in data.values()

def test_auth_config_save_and_load_round_trip(tmp_path):
    import json
    from core.platform_auth import (
        create_password_hash,
        load_auth_config,
        save_auth_config,
    )

    config_path = tmp_path / "platform_auth.json"
    user_hash = create_password_hash("1234")
    admin_hash = create_password_hash("1234567", admin=True)

    save_auth_config(user_hash, admin_hash, config_path)
    loaded = load_auth_config(config_path)

    assert loaded["user_password_hash"] == user_hash
    assert loaded["admin_password_hash"] == admin_hash
    assert isinstance(loaded["session_secret_key"], str)
    assert len(loaded["session_secret_key"]) == 64
    stored = json.loads(config_path.read_text(encoding="utf-8"))
    assert loaded["session_secret_key"] == stored["session_secret_key"]
    import pytest
    from core.platform_auth import load_auth_config
    missing_path = tmp_path / 'missing.json'
    with pytest.raises(FileNotFoundError):
        load_auth_config(missing_path)
    incomplete_path = tmp_path / 'incomplete.json'
    incomplete_path.write_text(json.dumps({'user_password_hash': 'user-hash'}), encoding='utf-8')
    with pytest.raises(ValueError):
        load_auth_config(incomplete_path)


def test_authenticate_user_and_admin_passwords(tmp_path):
    from core.platform_auth import authenticate_password, create_password_hash, save_auth_config
    config_path = tmp_path / 'platform_auth.json'
    save_auth_config(create_password_hash('1234'), create_password_hash('1234567', admin=True), config_path)
    assert authenticate_password('1234', path=config_path) is True
    assert authenticate_password('9999', path=config_path) is False
    assert authenticate_password('1234567', admin=True, path=config_path) is True
    assert authenticate_password('7654321', admin=True, path=config_path) is False


def test_session_secret_key_is_secure_and_unique():
    from core.platform_auth import create_session_secret_key
    first_key = create_session_secret_key()
    second_key = create_session_secret_key()
    assert isinstance(first_key, str)
    assert len(first_key) == 64
    assert first_key != second_key


def test_auth_config_includes_session_secret_key(tmp_path):
    from core.platform_auth import create_password_hash, save_auth_config
    import json
    config_path = tmp_path / 'platform_auth.json'
    save_auth_config(create_password_hash('1234'), create_password_hash('1234567', admin=True), config_path)
    data = json.loads(config_path.read_text(encoding='utf-8'))
    assert isinstance(data['session_secret_key'], str)
    assert len(data['session_secret_key']) == 64


def test_auth_config_preserves_session_secret_key_on_resave(tmp_path):
    from core.platform_auth import create_password_hash, save_auth_config
    import json
    config_path = tmp_path / 'platform_auth.json'
    save_auth_config(create_password_hash('1234'), create_password_hash('1234567', admin=True), config_path)
    first_key = json.loads(config_path.read_text(encoding='utf-8'))['session_secret_key']
    save_auth_config(create_password_hash('5678'), create_password_hash('1234567', admin=True), config_path)
    second_key = json.loads(config_path.read_text(encoding='utf-8'))['session_secret_key']
    assert second_key == first_key


def test_auth_config_rejects_missing_or_incomplete_config(tmp_path):
    import json
    import pytest
    from core.platform_auth import load_auth_config
    missing_path = tmp_path / 'missing.json'
    with pytest.raises(FileNotFoundError):
        load_auth_config(missing_path)
    incomplete_path = tmp_path / 'incomplete.json'
    incomplete_path.write_text(json.dumps({'user_password_hash': 'user-hash'}), encoding='utf-8')
    with pytest.raises(ValueError):
        load_auth_config(incomplete_path)


def test_auth_config_rejects_missing_session_secret_key(tmp_path):
    import json
    import pytest
    from core.platform_auth import create_password_hash, load_auth_config
    config_path = tmp_path / 'platform_auth.json'
    config_path.write_text(json.dumps({'user_password_hash': create_password_hash('1234'), 'admin_password_hash': create_password_hash('1234567', admin=True)}), encoding='utf-8')
    with pytest.raises(ValueError, match='session secret key'):
        load_auth_config(config_path)

def test_configure_flask_auth_applies_stored_session_secret_key(tmp_path):
    from flask import Flask
    from core.platform_auth import create_password_hash, save_auth_config, configure_flask_auth

    config_path = tmp_path / "platform_auth.json"
    save_auth_config(
        create_password_hash("1234"),
        create_password_hash("1234567", admin=True),
        config_path,
    )

    app = Flask(__name__)
    config = configure_flask_auth(app, config_path)

    assert app.secret_key == config["session_secret_key"]
    assert len(app.secret_key) == 64

def test_configure_flask_auth_fails_closed_without_auth_config(tmp_path):
    import pytest
    from flask import Flask
    from core.platform_auth import configure_flask_auth

    app = Flask(__name__)
    missing_path = tmp_path / "missing-platform-auth.json"

    with pytest.raises(FileNotFoundError):
        configure_flask_auth(app, missing_path)

def test_user_login_api_creates_authenticated_session(tmp_path, monkeypatch):
    import api_server
    from core.platform_auth import create_password_hash, save_auth_config, configure_flask_auth

    config_path = tmp_path / "platform_auth.json"
    save_auth_config(
        create_password_hash("1234"),
        create_password_hash("1234567", admin=True),
        config_path,
    )

    configure_flask_auth(api_server.app, config_path)
    monkeypatch.setattr(api_server, "AUTH_CONFIG_PATH", config_path, raising=False)

    client = api_server.app.test_client()
    response = client.post("/api/auth/login", json={"password": "1234"})

    assert response.status_code == 200
    assert response.get_json()["success"] is True

    with client.session_transaction() as flask_session:
        assert flask_session["authenticated"] is True
        assert flask_session["role"] == "user"

def test_user_login_api_rejects_wrong_password(tmp_path, monkeypatch):
    import api_server
    from core.platform_auth import create_password_hash, save_auth_config, configure_flask_auth

    config_path = tmp_path / "platform_auth.json"
    save_auth_config(
        create_password_hash("1234"),
        create_password_hash("1234567", admin=True),
        config_path,
    )

    configure_flask_auth(api_server.app, config_path)
    monkeypatch.setattr(api_server, "AUTH_CONFIG_PATH", config_path)

    client = api_server.app.test_client()
    response = client.post("/api/auth/login", json={"password": "9999"})

    assert response.status_code == 401
    assert response.get_json()["success"] is False

    with client.session_transaction() as flask_session:
        assert "authenticated" not in flask_session
        assert "role" not in flask_session

def test_admin_login_api_creates_admin_session(tmp_path, monkeypatch):
    import api_server
    from core.platform_auth import create_password_hash, save_auth_config, configure_flask_auth

    config_path = tmp_path / "platform_auth.json"
    save_auth_config(
        create_password_hash("1234"),
        create_password_hash("1234567", admin=True),
        config_path,
    )

    configure_flask_auth(api_server.app, config_path)
    monkeypatch.setattr(api_server, "AUTH_CONFIG_PATH", config_path)

    client = api_server.app.test_client()
    response = client.post("/api/auth/admin-login", json={"password": "1234567"})

    assert response.status_code == 200
    assert response.get_json()["success"] is True

    with client.session_transaction() as flask_session:
        assert flask_session["authenticated"] is True
        assert flask_session["role"] == "admin"

def test_admin_login_api_rejects_wrong_password(tmp_path, monkeypatch):
    import api_server
    from core.platform_auth import create_password_hash, save_auth_config, configure_flask_auth

    config_path = tmp_path / "platform_auth.json"
    save_auth_config(
        create_password_hash("1234"),
        create_password_hash("1234567", admin=True),
        config_path,
    )

    configure_flask_auth(api_server.app, config_path)
    monkeypatch.setattr(api_server, "AUTH_CONFIG_PATH", config_path)

    client = api_server.app.test_client()
    response = client.post("/api/auth/admin-login", json={"password": "7654321"})

    assert response.status_code == 401
    assert response.get_json()["success"] is False

    with client.session_transaction() as flask_session:
        assert "authenticated" not in flask_session
        assert "role" not in flask_session

def test_logout_api_clears_authenticated_session(tmp_path, monkeypatch):
    import api_server
    from core.platform_auth import create_password_hash, save_auth_config, configure_flask_auth

    config_path = tmp_path / "platform_auth.json"
    save_auth_config(
        create_password_hash("1234"),
        create_password_hash("1234567", admin=True),
        config_path,
    )

    configure_flask_auth(api_server.app, config_path)
    monkeypatch.setattr(api_server, "AUTH_CONFIG_PATH", config_path)

    client = api_server.app.test_client()

    login_response = client.post("/api/auth/login", json={"password": "1234"})
    assert login_response.status_code == 200

    logout_response = client.post("/api/auth/logout")

    assert logout_response.status_code == 200
    assert logout_response.get_json()["success"] is True

    with client.session_transaction() as flask_session:
        assert "authenticated" not in flask_session
        assert "role" not in flask_session

def test_auth_status_api_reports_authenticated_user(tmp_path, monkeypatch):
    import api_server
    from core.platform_auth import create_password_hash, save_auth_config, configure_flask_auth

    config_path = tmp_path / "platform_auth.json"
    save_auth_config(
        create_password_hash("1234"),
        create_password_hash("1234567", admin=True),
        config_path,
    )

    configure_flask_auth(api_server.app, config_path)
    monkeypatch.setattr(api_server, "AUTH_CONFIG_PATH", config_path)

    client = api_server.app.test_client()

    login_response = client.post("/api/auth/login", json={"password": "1234"})
    assert login_response.status_code == 200

    status_response = client.get("/api/auth/status")

    assert status_response.status_code == 200
    assert status_response.get_json() == {
        "authenticated": True,
        "role": "user",
    }

def test_auth_status_api_reports_unauthenticated_session(tmp_path, monkeypatch):
    import api_server
    from core.platform_auth import create_password_hash, save_auth_config, configure_flask_auth

    config_path = tmp_path / "platform_auth.json"
    save_auth_config(
        create_password_hash("1234"),
        create_password_hash("1234567", admin=True),
        config_path,
    )

    configure_flask_auth(api_server.app, config_path)
    monkeypatch.setattr(api_server, "AUTH_CONFIG_PATH", config_path)

    client = api_server.app.test_client()
    response = client.get("/api/auth/status")

    assert response.status_code == 200
    assert response.get_json() == {
        "authenticated": False,
        "role": None,
    }

def test_update_user_password_preserves_admin_hash_and_session_key(tmp_path):
    from core.platform_auth import (
        authenticate_password,
        create_password_hash,
        load_auth_config,
        save_auth_config,
        update_user_password,
    )

    config_path = tmp_path / "platform_auth.json"
    save_auth_config(
        create_password_hash("1234"),
        create_password_hash("1234567", admin=True),
        config_path,
    )

    before = load_auth_config(config_path)

    update_user_password("5678", config_path)

    after = load_auth_config(config_path)

    assert after["admin_password_hash"] == before["admin_password_hash"]
    assert after["session_secret_key"] == before["session_secret_key"]
    assert authenticate_password("5678", path=config_path) is True
    assert authenticate_password("1234", path=config_path) is False
    assert authenticate_password("1234567", admin=True, path=config_path) is True

def test_user_password_change_api_rejects_non_admin(tmp_path, monkeypatch):
    import api_server
    from core.platform_auth import create_password_hash, save_auth_config, configure_flask_auth

    config_path = tmp_path / "platform_auth.json"
    save_auth_config(
        create_password_hash("1234"),
        create_password_hash("1234567", admin=True),
        config_path,
    )

    configure_flask_auth(api_server.app, config_path)
    monkeypatch.setattr(api_server, "AUTH_CONFIG_PATH", config_path)

    client = api_server.app.test_client()

    login_response = client.post("/api/auth/login", json={"password": "1234"})
    assert login_response.status_code == 200

    response = client.post(
        "/api/auth/user-password",
        json={"password": "5678"},
    )

    assert response.status_code == 403
    assert response.get_json()["success"] is False

def test_admin_can_change_user_password(tmp_path, monkeypatch):
    import api_server
    from core.platform_auth import (
        authenticate_password,
        create_password_hash,
        save_auth_config,
        configure_flask_auth,
    )

    config_path = tmp_path / "platform_auth.json"
    save_auth_config(
        create_password_hash("1234"),
        create_password_hash("1234567", admin=True),
        config_path,
    )

    configure_flask_auth(api_server.app, config_path)
    monkeypatch.setattr(api_server, "AUTH_CONFIG_PATH", config_path)

    client = api_server.app.test_client()

    admin_login = client.post(
        "/api/auth/admin-login",
        json={"password": "1234567"},
    )
    assert admin_login.status_code == 200

    response = client.post(
        "/api/auth/user-password",
        json={"password": "5678"},
    )

    assert response.status_code == 200
    assert response.get_json()["success"] is True
    assert authenticate_password("5678", path=config_path) is True
    assert authenticate_password("1234", path=config_path) is False
    assert authenticate_password("1234567", admin=True, path=config_path) is True

def test_admin_user_password_change_rejects_invalid_format(tmp_path, monkeypatch):
    import api_server
    from core.platform_auth import (
        authenticate_password,
        create_password_hash,
        save_auth_config,
        configure_flask_auth,
    )

    config_path = tmp_path / "platform_auth.json"
    save_auth_config(
        create_password_hash("1234"),
        create_password_hash("1234567", admin=True),
        config_path,
    )

    configure_flask_auth(api_server.app, config_path)
    monkeypatch.setattr(api_server, "AUTH_CONFIG_PATH", config_path)

    client = api_server.app.test_client()

    admin_login = client.post(
        "/api/auth/admin-login",
        json={"password": "1234567"},
    )
    assert admin_login.status_code == 200

    response = client.post(
        "/api/auth/user-password",
        json={"password": "56789"},
    )

    assert response.status_code == 400
    assert response.get_json()["success"] is False
    assert authenticate_password("1234", path=config_path) is True
    assert authenticate_password("1234567", admin=True, path=config_path) is True

def test_user_password_change_api_rejects_unauthenticated(tmp_path, monkeypatch):
    import api_server
    from core.platform_auth import create_password_hash, save_auth_config, configure_flask_auth

    config_path = tmp_path / "platform_auth.json"
    save_auth_config(
        create_password_hash("1234"),
        create_password_hash("1234567", admin=True),
        config_path,
    )

    configure_flask_auth(api_server.app, config_path)
    monkeypatch.setattr(api_server, "AUTH_CONFIG_PATH", config_path)

    client = api_server.app.test_client()

    response = client.post(
        "/api/auth/user-password",
        json={"password": "5678"},
    )

    assert response.status_code == 401
    assert response.get_json()["success"] is False

def test_ranking_api_rejects_unauthenticated_request(tmp_path, monkeypatch):
    import api_server
    from core.platform_auth import create_password_hash, save_auth_config, configure_flask_auth

    config_path = tmp_path / "platform_auth.json"
    save_auth_config(
        create_password_hash("1234"),
        create_password_hash("1234567", admin=True),
        config_path,
    )

    configure_flask_auth(api_server.app, config_path)
    monkeypatch.setattr(api_server, "AUTH_CONFIG_PATH", config_path)

    client = api_server.app.test_client()
    response = client.get("/api/ranking")

    assert response.status_code == 401
    assert response.get_json()["success"] is False
