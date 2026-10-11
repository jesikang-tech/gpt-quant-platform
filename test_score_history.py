"""Synthetic DB query and output contract; no operational DB entry point."""
from contextlib import closing
from price_test_support import isolated_price_db, phase8_test_scope


def _print_history(conn):
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT *
        FROM etf_score_history
        ORDER BY id DESC
        LIMIT 5
        """
    )


    rows = cursor.fetchall()


    print("=" * 40)
    print("ETF Score History")
    print("=" * 40)


    for row in rows:
        print(row)



    return rows


def test_score_history(isolated_price_db, capsys):
    with phase8_test_scope(isolated_price_db) as scope:
        payloads = [("TEST", i * 2.0, i * 3.0, float(i), i * 6.0, f"2026-01-{i:02d}") for i in range(1, 8)]
        for payload in payloads:
            scope.repository.save_score_history(*payload)
        before = isolated_price_db.path.read_bytes()
        with closing(scope.database.get_connection()) as conn:
            rows = _print_history(conn)
        expected = [(i, *payloads[i - 1]) for i in range(7, 2, -1)]
        assert rows == expected
        assert len(rows) == 5
        output = capsys.readouterr().out
        assert "ETF Score History" in output
        assert [line for line in output.splitlines() if line.startswith("(")] == [str(row) for row in expected]
        assert isolated_price_db.path.read_bytes() == before
