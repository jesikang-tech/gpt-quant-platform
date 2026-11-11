"""Offline safety tests for the isolated UAT launcher."""

import importlib
from unittest.mock import Mock

import pytest


def test_import_does_not_start_server(monkeypatch):
    from flask import Flask

    run = Mock()
    monkeypatch.setattr(Flask, "run", run)

    import uat_boundary.launch as launch

    importlib.reload(launch)

    run.assert_not_called()


def test_missing_password_fails_closed(monkeypatch):
    from uat_boundary import launch

    monkeypatch.delenv("KIWOOM_UAT_PASSWORD", raising=False)
    monkeypatch.setenv("KIWOOM_UAT_SESSION_SECRET", "s" * 40)

    with pytest.raises(RuntimeError, match="password"):
        launch.main()


def test_missing_session_secret_fails_closed(monkeypatch):
    from uat_boundary import launch

    monkeypatch.setenv("KIWOOM_UAT_PASSWORD", "test-only-password")
    monkeypatch.delenv("KIWOOM_UAT_SESSION_SECRET", raising=False)

    with pytest.raises(RuntimeError, match="session secret"):
        launch.main()


def test_short_session_secret_fails_closed(monkeypatch):
    from uat_boundary import launch

    monkeypatch.setenv("KIWOOM_UAT_PASSWORD", "test-only-password")
    monkeypatch.setenv("KIWOOM_UAT_SESSION_SECRET", "short")

    with pytest.raises(RuntimeError, match="session secret"):
        launch.main()


def test_launcher_uses_loopback_without_starting_server(monkeypatch):
    from uat_boundary import launch

    fake_app = Mock()
    build = Mock(return_value=fake_app)

    monkeypatch.setattr(launch, "build_launch_app", build)
    monkeypatch.setenv("KIWOOM_UAT_PASSWORD", "test-only-password")
    monkeypatch.setenv("KIWOOM_UAT_SESSION_SECRET", "s" * 40)

    launch.main()

    build.assert_called_once_with(
        password="test-only-password",
        session_secret="s" * 40,
    )

    fake_app.run.assert_called_once_with(
        host="127.0.0.1",
        port=5051,
        debug=False,
        use_reloader=False,
        threaded=False,
    )


def test_factory_reuse_without_server_start(monkeypatch):
    from uat_boundary import launch

    fake_app = object()
    factory = Mock(return_value=fake_app)

    monkeypatch.setattr(launch, "create_uat_app", factory)

    result = launch.build_launch_app(
        password="test-only-password",
        session_secret="s" * 40,
    )

    assert result is fake_app

    factory.assert_called_once_with(
        password="test-only-password",
        session_secret="s" * 40,
    )