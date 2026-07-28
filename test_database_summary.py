from database import get_connection


def main():
    conn = get_connection()
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

    for ticker, cnt in cursor.fetchall():
        print(f"{ticker} : {cnt}")

    conn.close()

    print("\n" + "=" * 60)
    print("Database Summary Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()