"""Real repository query and output contract using guarded synthetic data."""
from price_test_support import isolated_price_db, phase8_test_scope


def _print_detail(result):
    print('=' * 40)
    print('ETF Score Detail')
    print('=' * 40)
    print(result)


def test_score_detail(isolated_price_db, capsys):
    with phase8_test_scope(isolated_price_db) as scope:
        ticker = "365040"
        old = (ticker, 10, 20, 30, 60, "2026-07-30")
        latest_id = (ticker, 20, 30, 40, 90, "2026-07-29")
        with scope.database.get_connection() as conn:
            conn.executemany("INSERT INTO etf_scores(ticker, return_score, trend_score, slope_score, "
                             "final_score, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                             [old, latest_id, ("OTHER", 99, 99, 99, 99, "2026-07-31")])
        # Connection context commits; scope guarantees closure even on failure.
        conn.close()
        before = isolated_price_db.path.read_bytes()
        result = scope.repository.get_etf_score_detail(ticker)
        _print_detail(result)
        assert result == latest_id
        output = capsys.readouterr().out
        assert "ETF Score Detail" in output
        assert str(result) in output
        assert scope.repository.get_etf_score_detail("MISSING") is None
        assert isolated_price_db.path.read_bytes() == before
