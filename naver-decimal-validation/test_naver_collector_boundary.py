"""Fail-first NAVER collector test with isolated import dependencies."""

import importlib.util
import sys
import types
from pathlib import Path

import pandas as pd
import pytest

from core.price_provenance_gate import PriceProvenanceRejected


def test_naver_provider_cannot_reach_legacy_price_writers(monkeypatch):
    calls = []

    def forbidden_write(*args, **kwargs):
        calls.append((args, kwargs))
        raise AssertionError("Legacy price writer must not execute")

    fake_fdr = types.ModuleType("providers.fdr_provider")

    class FakeFDRProvider:
        def get_price(self, *args, **kwargs):
            raise AssertionError("Real FDR provider must not execute")

    fake_fdr.FDRProvider = FakeFDRProvider

    fake_repository = types.ModuleType("repository")
    fake_repository.save_etf_price = forbidden_write
    fake_repository.save_etf_ohlcv_price = forbidden_write

    fake_providers = types.ModuleType("providers")
    fake_providers.__path__ = []

    with monkeypatch.context() as patch:
        patch.setitem(sys.modules, "providers", fake_providers)
        patch.setitem(sys.modules, "providers.fdr_provider", fake_fdr)
        patch.setitem(sys.modules, "repository", fake_repository)

        source = (
            Path(__file__).resolve().parent
            / "integration_sources"
            / "price_collector.py"
        )

        spec = importlib.util.spec_from_file_location(
            "_isolated_naver_price_collector", source
        )
        assert spec is not None and spec.loader is not None

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        class UnverifiedNaverProvider:
            provider = "NAVER"

            def get_price(self, ticker, start_date, end_date):
                return pd.DataFrame(
                    {
                        "Open": [99],
                        "High": [105],
                        "Low": [98],
                        "Close": [100],
                        "Volume": [10],
                    },
                    index=pd.to_datetime(["2026-01-02"]),
                )

        collector = module.PriceCollector()
        collector.provider = UnverifiedNaverProvider()

        with pytest.raises(PriceProvenanceRejected):
            collector.collect("111111", "2026-01-01", "2026-01-05")

    assert calls == []
