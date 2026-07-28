from database import init_database, get_connection
from collector.etf_collector import ETFCollector


# DB 초기화
init_database()


# ETF 수집 및 저장
collector = ETFCollector()
collector.collect()


# 저장 결과 확인
conn = get_connection()
cursor = conn.cursor()

cursor.execute(
    """
    SELECT COUNT(*)
    FROM etf_info
    """
)

count = cursor.fetchone()[0]

conn.close()


print(f"DB 저장 ETF 개수 : {count}")