"""Direct provider denial without importing the external FDR library."""

import importlib.util
from pathlib import Path
import sys
from types import ModuleType

import pytest

from core.price_provenance_gate import (
    PriceProvenanceRejected,
    assess_price_provenance,
    require_persistence_authorization,
)


def test_direct_fdr_price_fetch_rejects_before_datareader(monkeypatch):
    root = Path(__file__).resolve().parent
    calls = {"DataReader": 0, "StockListing": 0}

    def forbidden(name):
        def fail(*args, **kwargs):
            calls[name] += 1
            raise AssertionError(f"External provider access forbidden: {name}")
        return fail

    with monkeypatch.context() as patch:
        external = ModuleType("FinanceDataReader")
        external.DataReader = forbidden("DataReader")
        external.StockListing = forbidden("StockListing")
        patch.setitem(sys.modules, "FinanceDataReader", external)
        # Use an isolated package to preserve any previously imported providers.
        package = ModuleType("_fdr_provenance_subject")
        package.__path__ = []
        patch.setitem(sys.modules, package.__name__, package)

        def load_source(name):
            qualified = f"{package.__name__}.{name}"
            spec = importlib.util.spec_from_file_location(
                qualified, root / "providers" / f"{name}.py",
            )
            module = importlib.util.module_from_spec(spec)
            patch.setitem(sys.modules, qualified, module)
            spec.loader.exec_module(module)
            return module

        load_source("base_provider")
        provider_module = load_source("fdr_provider")
        assert provider_module.assess_price_provenance is assess_price_provenance
        assert provider_module.require_persistence_authorization is require_persistence_authorization
        assert provider_module.fdr is external
        assert calls == {"DataReader": 0, "StockListing": 0}
        with pytest.raises(PriceProvenanceRejected) as rejected:
            provider_module.FDRProvider().get_price(
                "SYNTHETIC", "2026-01-01", "2026-01-02",
            )
        assert str(rejected.value) == (
            "Price provenance is unverified; persistence is prohibited"
        )
        assert calls == {"DataReader": 0, "StockListing": 0}
