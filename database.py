import sqlite3
import os

from config import DB_PATH


def get_connection():
    """
    SQLite 데이터베이스 연결
    """

    os.makedirs(
        os.path.dirname(DB_PATH),
        exist_ok=True
    )

    conn = sqlite3.connect(DB_PATH)

    return conn


def initialize_database():
    """
    데이터베이스 초기 테이블 생성
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS etf_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL,
            date TEXT NOT NULL,
            close_price REAL NOT NULL
        )
        """
    )

    conn.commit()
    conn.close()