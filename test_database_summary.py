"""Synthetic DB query and output contract; no operational DB entry point."""
from contextlib import closing
from price_test_support import isolated_price_db, phase8_test_scope


def _print_summary(conn):
    cursor = conn.cursor()

    print("=" * 60)
    print("GPT Quant Platform - Database Summary")
    print("=" * 60)

    # ETF 정보 개수
    cursor.execute("""
        SELECT COUNT(*)
        FROM etf_info
    """)
    etf_count = cursor.fetchone()[0]

    print(f"\nETF 정보 개수 : {etf_count}")

    # 가격 데이터 개수
    cursor.execute("""
        SELECT COUNT(*)
        FROM etf_prices
    """)
    price_count = cursor.fetchone()[0]

    print(f"가격 데이터 개수 : {price_count}")

    # 가격 데이터가 있는 ETF 개수
    cursor.execute("""
        SELECT COUNT(DISTINCT ticker)
        FROM etf_prices
    """)
    price_etf_count = cursor.fetchone()[0]

    print(f"가격 데이터 보유 ETF : {price_etf_count}")

    # 가격 데이터가 없는 ETF 개수
    cursor.execute("""
        SELECT COUNT(*)
        FROM etf_info
        WHERE ticker NOT IN (
            SELECT DISTINCT ticker
            FROM etf_prices
        )
    """)
    no_price_count = cursor.fetchone()[0]

    print(f"가격 데이터 없는 ETF : {no_price_count}")

    # 상위 5개 가격 데이터 건수
    cursor.execute("""
        SELECT
            ticker,
            COUNT(*) AS cnt
        FROM etf_prices
        GROUP BY ticker
        ORDER BY cnt DESC
        LIMIT 5
    """)

    print("\n상위 5개 가격 데이터")

    top_rows = cursor.fetchall()
    for ticker, cnt in top_rows:
        print(f"{ticker} : {cnt}")


    print("\n" + "=" * 60)
    print("Database Summary Complete")
    print("=" * 60)

    return etf_count, price_count, price_etf_count, no_price_count, top_rows


def test_database_summary(isolated_price_db, capsys):
    with phase8_test_scope(isolated_price_db) as scope:
        counts = {f"TEST{i}": i for i in range(1, 7)}
        with closing(scope.database.get_connection()) as conn:
            with conn:
                conn.executemany("INSERT INTO etf_info(ticker, name, market) VALUES (?, ?, 'TEST')",
                                 [(ticker, ticker) for ticker in [*counts, "NO_PRICE"]])
                conn.executemany("INSERT INTO etf_prices VALUES (?, ?, ?)",
                                 [(ticker, f"2026-01-{day:02d}", 100 + day)
                                  for ticker, count in counts.items() for day in range(1, count + 1)])
        before = isolated_price_db.path.read_bytes()
        with closing(scope.database.get_connection()) as conn:
            summary = _print_summary(conn)
        expected_top = sorted(counts.items(), key=lambda item: item[1], reverse=True)[:5]
        assert summary == (len(counts) + 1, sum(counts.values()), len(counts), 1, expected_top)
        output = capsys.readouterr().out
        assert "Database Summary Complete" in output
        assert "ETF 정보 개수 : 7" in output
        assert "가격 데이터 개수 : 21" in output
        assert "가격 데이터 보유 ETF : 6" in output
        assert "가격 데이터 없는 ETF : 1" in output
        assert [line for line in output.splitlines() if line.startswith("TEST")] == [
            f"{ticker} : {count}" for ticker, count in expected_top]
        assert isolated_price_db.path.read_bytes() == before
