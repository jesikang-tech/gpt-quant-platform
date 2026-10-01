"""Authentication primitives for GPT Quant Platform."""

import json
import secrets
from pathlib import Path

from werkzeug.security import check_password_hash, generate_password_hash


USER_PASSWORD_LENGTH = 4
ADMIN_PASSWORD_LENGTH = 7
DEFAULT_AUTH_CONFIG_PATH = Path("config") / "platform_auth.json"


def validate_password_format(password: str, *, admin: bool = False) -> bool:
    """Return True only when password is numeric and has the required length."""
    if not isinstance(password, str):
        return False

    required_length = ADMIN_PASSWORD_LENGTH if admin else USER_PASSWORD_LENGTH

    return len(password) == required_length and password.isascii() and password.isdigit()


def create_password_hash(password: str, *, admin: bool = False) -> str:
    """Validate a platform password and return its secure hash."""
    if not validate_password_format(password, admin=admin):
        raise ValueError("invalid password format")

    return generate_password_hash(password)


def verify_password(password_hash: str, password: str, *, admin: bool = False) -> bool:
    """Validate the supplied password format and compare it with a stored hash."""
    if not isinstance(password_hash, str) or not password_hash:
        return False

    if not validate_password_format(password, admin=admin):
        return False

    return check_password_hash(password_hash, password)

def save_auth_config(
    user_password_hash: str,
    admin_password_hash: str,
    path: Path = DEFAULT_AUTH_CONFIG_PATH,
) -> None:
    """Persist only password hashes to the local authentication config."""
    if not isinstance(user_password_hash, str) or not user_password_hash:
        raise ValueError("user password hash is required")

    if not isinstance(admin_password_hash, str) or not admin_password_hash:
        raise ValueError("admin password hash is required")

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    session_secret_key = create_session_secret_key()
    if path.is_file():
        existing_data = json.loads(path.read_text(encoding="utf-8"))
        existing_session_secret_key = existing_data.get("session_secret_key")
        if isinstance(existing_session_secret_key, str) and existing_session_secret_key:
            session_secret_key = existing_session_secret_key

    data = {
        "user_password_hash": user_password_hash,
        "admin_password_hash": admin_password_hash,
        "session_secret_key": session_secret_key,
    }

    path.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8",
    )

def load_auth_config(path: Path = DEFAULT_AUTH_CONFIG_PATH) -> dict:
    """Load password hashes from the local authentication config."""
    path = Path(path)

    if not path.is_file():
        raise FileNotFoundError(f"authentication config not found: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(data, dict):
        raise ValueError("invalid authentication config")

    user_password_hash = data.get("user_password_hash")
    admin_password_hash = data.get("admin_password_hash")
    session_secret_key = data.get("session_secret_key")

    if not isinstance(user_password_hash, str) or not user_password_hash:
        raise ValueError("user password hash is missing")

    if not isinstance(admin_password_hash, str) or not admin_password_hash:
        raise ValueError("admin password hash is missing")

    if not isinstance(session_secret_key, str) or len(session_secret_key) != 64:
        raise ValueError("session secret key is missing or invalid")

    return {
        "user_password_hash": user_password_hash,
        "admin_password_hash": admin_password_hash,
        "session_secret_key": session_secret_key,
    }

def authenticate_password(password: str, *, admin: bool = False, path: Path = DEFAULT_AUTH_CONFIG_PATH) -> bool:
    """Verify a user or administrator password against the stored authentication config."""
    config = load_auth_config(path)
    hash_key = "admin_password_hash" if admin else "user_password_hash"
    return verify_password(config[hash_key], password, admin=admin)



def create_session_secret_key() -> str:
    """Generate a cryptographically secure secret key for Flask sessions."""
    return secrets.token_hex(32)


def configure_flask_auth(app, path: Path = DEFAULT_AUTH_CONFIG_PATH) -> dict:
    """Apply the stored authentication session secret to a Flask app."""
    config = load_auth_config(path)
    app.secret_key = config["session_secret_key"]
    return config

def update_user_password(password: str, path: Path = DEFAULT_AUTH_CONFIG_PATH) -> None:
    """Update only the user password while preserving admin credentials and session secret."""
    config = load_auth_config(path)
    user_password_hash = create_password_hash(password)
    save_auth_config(
        user_password_hash,
        config["admin_password_hash"],
        path,
    )
