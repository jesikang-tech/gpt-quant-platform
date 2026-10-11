"""Real repository query and output contract using guarded synthetic data."""
from price_test_support import isolated_price_db, phase8_test_scope


def _print_snapshot(results):
    print('=' * 40)
    print('ETF Ranking Snapshot')
    print('=' * 40)
    for row in results:
        print(row)


def test_ranking_snapshot(isolated_price_db, capsys):
    with phase8_test_scope(isolated_price_db) as scope:
        day = "2026-07-30"
        entries = [("TEST_A", 3, 60), ("TEST_B", 1, 90), ("TEST_C", 2, 75)]
        for ticker, rank, score in entries:
            scope.repository.save_ranking_history(ticker, rank, score, day)
        scope.repository.save_ranking_history("OTHER_DAY", 1, 99, "2026-07-29")
        before = isolated_price_db.path.read_bytes()
        results = scope.repository.get_ranking_snapshot(day)
        _print_snapshot(results)
        expected = sorted(entries, key=lambda item: item[1])
        assert results == expected
        output = capsys.readouterr().out
        assert "ETF Ranking Snapshot" in output
        assert [line for line in output.splitlines() if line.startswith("(")] == [str(row) for row in results]
        assert scope.repository.get_ranking_snapshot("2026-07-31") == []
        assert isolated_price_db.path.read_bytes() == before
