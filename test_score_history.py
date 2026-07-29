from database import get_connection


def main():

    conn = get_connection()
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


    conn.close()



if __name__ == "__main__":
    main()