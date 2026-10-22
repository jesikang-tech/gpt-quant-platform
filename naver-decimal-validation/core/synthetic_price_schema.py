"""Strict schema contract for synthetic ETF price tables.

Does not open connections, modify schema or authorize database access.
"""

import sqlite3


class SyntheticSchemaRejected(RuntimeError):
    pass


EXPECTED = {
    "etf_prices": (
        ("ticker", "TEXT", 1, 1),
        ("date", "TEXT", 1, 2),
        ("close_price", "REAL", 1, 0),
    ),
    "etf_ohlcv_prices": (
        ("ticker", "TEXT", 1, 1),
        ("date", "TEXT", 1, 2),
        ("open_price", "REAL", 0, 0),
        ("high_price", "REAL", 0, 0),
        ("low_price", "REAL", 0, 0),
        ("close_price", "REAL", 0, 0),
        ("volume", "REAL", 0, 0),
    ),
}


def validate_synthetic_price_schema(conn):
    if type(conn) is not sqlite3.Connection:
        raise SyntheticSchemaRejected("SQLite connection required")

    for table, expected in EXPECTED.items():
        rows = conn.execute(
            "SELECT type FROM main.sqlite_master "
            "WHERE name = ?",
            (table,),
        ).fetchall()

        if rows != [("table",)]:
            raise SyntheticSchemaRejected("Missing or invalid table")

        columns = conn.execute(
            f"PRAGMA main.table_info('{table}')"
        ).fetchall()

        actual = tuple(
            (row[1], row[2].upper(), row[3], row[5])
            for row in columns
        )

        if actual != expected:
            raise SyntheticSchemaRejected("Unexpected table schema")

    return True