"""Synthetic-only atomic ETF price persistence.

This module never opens a database or authorizes operational access.
Only a caller-owned, isolated SQLite in-memory connection is accepted.
"""

import sqlite3

from core.price_pair_contract import PricePair, prepare_price_pair
from core.synthetic_price_schema import validate_synthetic_price_schema


class SyntheticPriceWriteRejected(RuntimeError):
    pass


def _require_synthetic_connection(conn):
    if type(conn) is not sqlite3.Connection:
        raise SyntheticPriceWriteRejected("SQLite connection required")

    if conn.in_transaction:
        raise SyntheticPriceWriteRejected("Existing transaction prohibited")

    databases = conn.execute("PRAGMA database_list").fetchall()

    if (
        not databases
        or databases[0][1] != "main"
        or databases[0][2] != ""
        or len(databases) > 2
        or (
            len(databases) == 2
            and (
                databases[1][1] != "temp"
                or databases[1][2] != ""
            )
        )
    ):
        raise SyntheticPriceWriteRejected("Only isolated memory DB permitted")

    temp_objects = conn.execute(
        "SELECT name FROM temp.sqlite_master "
        "WHERE type IN ('table', 'view', 'trigger', 'index')"
    ).fetchall()

    if temp_objects:
        raise SyntheticPriceWriteRejected("TEMP schema objects prohibited")

    if conn.execute("PRAGMA query_only").fetchone()[0]:
        raise SyntheticPriceWriteRejected("Read-only connection prohibited")

    if conn.execute("PRAGMA ignore_check_constraints").fetchone()[0]:
        raise SyntheticPriceWriteRejected("Disabled constraints prohibited")

    for schema in ("main", "temp"):
        triggers = conn.execute(
            f"SELECT name FROM {schema}.sqlite_master "
            "WHERE type = 'trigger'"
        ).fetchall()

        if triggers:
            raise SyntheticPriceWriteRejected("Triggers prohibited")


def insert_synthetic_price_pair(conn, pair):
    """Insert both observations atomically; reject existing records."""

    if type(pair) is not PricePair:
        raise SyntheticPriceWriteRejected("Validated PricePair required")

    validated = prepare_price_pair(
        pair.ticker,
        pair.observation_date,
        pair.close_price,
        pair.open_price,
        pair.high_price,
        pair.low_price,
        pair.volume,
    )

    _require_synthetic_connection(conn)
    validate_synthetic_price_schema(conn)

    try:
        conn.execute("BEGIN IMMEDIATE")

        conn.execute(
            """
            INSERT INTO etf_prices (ticker, date, close_price)
            VALUES (?, ?, ?)
            """,
            (
                validated.ticker,
                validated.observation_date,
                validated.close_price,
            ),
        )

        conn.execute(
            """
            INSERT INTO etf_ohlcv_prices
                (ticker, date, open_price, high_price,
                 low_price, close_price, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                validated.ticker,
                validated.observation_date,
                validated.open_price,
                validated.high_price,
                validated.low_price,
                validated.close_price,
                validated.volume,
            ),
        )

        conn.commit()

    except BaseException:
        conn.rollback()
        raise