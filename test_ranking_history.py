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