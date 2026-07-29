import sqlite3
from config import DATABASE_PATH


def get_connection():
    return sqlite3.connect(
        DATABASE_PATH,
        timeout=30
        )


def init_database():
    conn = get_connection()
    cursor = conn.cursor()

    # ETF 가격
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS etf_prices (
        ticker TEXT NOT NULL,
        date TEXT NOT NULL,
        close_price REAL NOT NULL,
        PRIMARY KEY (ticker, date)
    )
    """)

    # ETF 기본정보
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS etf_info (
        ticker TEXT PRIMARY KEY,
        name TEXT,
        market TEXT
    )
    """)

    # ETF 점수
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS etf_scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker TEXT NOT NULL,
        return_score REAL,
        trend_score REAL,
        slope_score REAL,
        final_score REAL,
        created_at TEXT
    )
    """)

    # ETF Score History
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS etf_score_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker TEXT NOT NULL,
        return_score REAL,
        trend_score REAL,
        slope_score REAL,
        final_score REAL,
        analysis_date TEXT
    )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_database()
    print("Database initialized")