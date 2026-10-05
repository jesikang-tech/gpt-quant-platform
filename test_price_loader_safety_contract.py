from pathlib import Path


def test_price_loader_direct_execution_is_disabled():
    source = Path("price_loader.py").read_text(encoding="utf-8")

    assert 'if __name__ == "__main__":' in source
    assert "raise SystemExit(" in source
    assert "Direct execution against the operational database is disabled." in source


def test_price_loader_direct_execution_does_not_call_database_update():
    source = Path("price_loader.py").read_text(encoding="utf-8")

    main_start = source.index('if __name__ == "__main__":')
    main_source = source[main_start:]

    assert "get_csv_price_data()" not in main_source
    assert "update_price_database(" not in main_source
    assert "save_etf_price(" not in main_source
