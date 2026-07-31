from database import get_connection



def main():

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT *
        FROM etf_ranking_history
        ORDER BY id DESC
        LIMIT 10
        """
    )


    rows = cursor.fetchall()


    print("=" * 40)
    print("ETF Ranking History")
    print("=" * 40)


    for row in rows:
        print(row)


    conn.close()



if __name__ == "__main__":
    main()



def get_ranking_history(ticker):
    """
    ETF Ranking History 조회
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            rank,
            final_score,
            ranking_date
        FROM etf_ranking_history
        WHERE ticker = ?
        ORDER BY ranking_date DESC
    """, (ticker,))

    rows = cursor.fetchall()

    conn.close()

    return rows



from repository import get_ranking_history

print("\n===== Ranking History Query Test =====")

history = get_ranking_history("069500")

for row in history:
    print(row)