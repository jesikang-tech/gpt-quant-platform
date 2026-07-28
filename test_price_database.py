from database import get_connection


conn = get_connection()
cursor = conn.cursor()


cursor.execute(
    """
    SELECT COUNT(*)
    FROM etf_prices
    WHERE ticker = ?
    """,
    ("069500",)
)


count = cursor.fetchone()[0]


cursor.execute(
    """
    SELECT *
    FROM etf_prices
    WHERE ticker = ?
    ORDER BY date
    LIMIT 5
    """,
    ("069500",)
)


rows = cursor.fetchall()


conn.close()


print(f"069500 저장 데이터 개수 : {count}")

print()

for row in rows:
    print(row)