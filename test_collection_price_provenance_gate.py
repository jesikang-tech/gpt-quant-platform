"""Database-free behavioral tests of real collection entry provenance gates."""

import importlib.util
from pathlib import Path
import sqlite3
import sys
from types import ModuleType, SimpleNamespace

import pytest

from core.price_provenance_gate import (
    PriceProvenanceRejected,
    assess_price_provenance,
    require_persistence_authorization,
)


@pytest.fixture
def guarded_collection(monkeypatch, tmp_path):
    root = Path(__file__).resolve().parent
    calls = {}

    def forbidden(name):
        calls[name] = 0

        def fail(*args, **kwargs):
            calls[name] += 1
            raise AssertionError(f"Forbidden downstream operation: {name}")

        return fail

    with monkeypatch.context() as patch:
        # These test-local dependencies avoid config directory creation and
        # importing FinanceDataReader. No authorization function is replaced.
        config = ModuleType("config")
        config.DATABASE_PATH = tmp_path / "never-opened.db"
        database = ModuleType("database")
        database.get_connection = forbidden("database.get_connection")
        repository = ModuleType("repository")
        for name in ("save_etf_price", "save_etf_ohlcv_price", "has_price_data"):
            setattr(repository, name, forbidden(f"repository.{name}"))
        provider_module = ModuleType("providers.fdr_provider")

        class RecordingProvider:
            def __init__(self):
                self.get_price = forbidden(f"provider.{len(calls)}.get_price")

        provider_module.FDRProvider = RecordingProvider
        for name, module in (
            ("config", config), ("database", database),
            ("repository", repository), ("providers.fdr_provider", provider_module),
        ):
            patch.setitem(sys.modules, name, module)
        for name in ("providers", "collector"):
            package = ModuleType(name)
            package.__path__ = []
            patch.setitem(sys.modules, name, package)
        patch.setattr(sqlite3, "connect", forbidden("sqlite3.connect"))
        patch.setattr(sqlite3.dbapi2, "connect", forbidden("sqlite3.dbapi2.connect"))
        patch.setattr(sqlite3, "Connection", forbidden("sqlite3.Connection"))

        def load_collector(name):
            qualified = f"collector.{name}"
            spec = importlib.util.spec_from_file_location(
                qualified, root / "collector" / f"{name}.py",
            )
            module = importlib.util.module_from_spec(spec)
            patch.setitem(sys.modules, qualified, module)
            spec.loader.exec_module(module)
            assert module.assess_price_provenance is assess_price_provenance
            assert module.require_persistence_authorization is require_persistence_authorization
            return module

        price_module = load_collector("price_collector")
        bulk_module = load_collector("bulk_price_collector")
        incremental_module = load_collector("incremental_price_updater")
        price = price_module.PriceCollector()
        bulk = bulk_module.BulkPriceCollector()
        incremental = incremental_module.IncrementalPriceUpdater()
        patch.setattr(bulk, "get_etf_list", forbidden("bulk.discovery"))
        patch.setattr(bulk.price_collector, "collect", forbidden("bulk.delegation"))
        patch.setattr(incremental, "get_etf_list", forbidden("incremental.discovery"))
        patch.setattr(incremental, "get_latest_price_date", forbidden("incremental.latest_date"))
        patch.setattr(incremental.price_collector, "collect", forbidden("incremental.delegation"))
        assert all(count == 0 for count in calls.values())
        yield SimpleNamespace(
            price=price, bulk=bulk, incremental=incremental, calls=calls,
            patch=patch, forbidden=forbidden,
        )


def _assert_rejected(call, calls):
    with pytest.raises(PriceProvenanceRejected) as rejected:
        call()
    assert str(rejected.value) == (
        "Price provenance is unverified; persistence is prohibited"
    )
    assert calls
    assert all(count == 0 for count in calls.values()), calls


def test_price_collect_rejects_before_fetch_or_write(guarded_collection):
    guarded = guarded_collection
    _assert_rejected(
        lambda: guarded.price.collect("SYNTHETIC", "2026-01-01", "2026-01-02"),
        guarded.calls,
    )


def test_bulk_collect_rejects_before_discovery_or_delegation(guarded_collection):
    guarded = guarded_collection
    _assert_rejected(
        lambda: guarded.bulk.collect("2026-01-01", "2026-01-02", limit=1),
        guarded.calls,
    )


def test_update_ticker_rejects_before_latest_date_or_delegation(guarded_collection):
    guarded = guarded_collection
    _assert_rejected(
        lambda: guarded.incremental.update_ticker("SYNTHETIC", "2026-01-02"),
        guarded.calls,
    )


def test_update_all_rejects_before_discovery_or_ticker_processing(guarded_collection):
    guarded = guarded_collection
    guarded.patch.setattr(
        guarded.incremental, "update_ticker", guarded.forbidden("incremental.per_ticker"),
    )
    _assert_rejected(
        lambda: guarded.incremental.update_all("2026-01-02"), guarded.calls,
    )
