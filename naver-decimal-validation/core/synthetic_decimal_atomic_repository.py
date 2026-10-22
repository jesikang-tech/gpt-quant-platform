"""Synthetic-only atomic Decimal price storage.

Only caller-owned isolated SQLite memory databases are accepted.
No operational database connections, provider calls, or authorization.
Decimal values are stored as exact canonical text.
"""

from decimal import Decimal

from core.decimal_synthetic_bridge import DecimalPricePair
from core.synthetic_atomic_price_repository import (
    _require_synthetic_connection,
    SyntheticPriceWriteRejected,
)


class SyntheticDecimalWriteRejected(RuntimeError):
    pass


_COLUMNS = {
    "synthetic_decimal_prices": ("ticker", "date", "close_price"),
    "synthetic_decimal_ohlcv": (
        "ticker", "date", "open_price", "high_price", "low_price",
        "close_price", "volume",
    ),
}
_TABLE_SQL = {
    name: (
        f"CREATE TABLE {name} ("
        + ", ".join(f"{column} TEXT NOT NULL" for column in columns)
        + ", PRIMARY KEY (ticker, date))"
    )
    for name, columns in _COLUMNS.items()
}


def _normalized_sql(sql):
    # Deliberately accept only our DDL, modulo whitespace. Metadata alone
    # cannot expose CHECK, COLLATE, REFERENCES or conflict policy changes.
    return " ".join(sql.split()) if isinstance(sql, str) else None


def _validate_decimal_schema(conn):
    expected_objects = {}
    for name, sql in _TABLE_SQL.items():
        expected_objects[("table", name, name)] = _normalized_sql(sql)
        expected_objects[("index", f"sqlite_autoindex_{name}_1", name)] = None

    objects = conn.execute(
        "SELECT type, name, tbl_name, sql FROM main.sqlite_master"
    ).fetchall()
    actual_objects = {
        (kind, name, table): _normalized_sql(sql)
        for kind, name, table, sql in objects
    }
    if len(objects) != len(expected_objects) or actual_objects != expected_objects:
        raise SyntheticDecimalWriteRejected("Unexpected synthetic schema")

    # Identifiers below come exclusively from the fixed module allow list.
    for name, columns in _COLUMNS.items():
        expected_columns = [
            (position, column, "TEXT", 1, None,
             position + 1 if position < 2 else 0, 0)
            for position, column in enumerate(columns)
        ]
        if conn.execute(f"PRAGMA main.table_xinfo('{name}')").fetchall() != expected_columns:
            raise SyntheticDecimalWriteRejected("Unexpected column definition")

        index = f"sqlite_autoindex_{name}_1"
        if conn.execute(f"PRAGMA main.index_list('{name}')").fetchall() != [
            (0, index, 1, "pk", 0)
        ]:
            raise SyntheticDecimalWriteRejected("Unexpected index definition")
        if conn.execute(f"PRAGMA main.index_xinfo('{index}')").fetchall() != [
            (0, 0, "ticker", 0, "BINARY", 1),
            (1, 1, "date", 0, "BINARY", 1),
            (2, -1, None, 0, "BINARY", 0),
        ]:
            raise SyntheticDecimalWriteRejected("Unexpected primary key definition")


def _exact_text(value):
    if type(value) is not Decimal or not value.is_finite():
        raise SyntheticDecimalWriteRejected("Finite Decimal required")

    return str(value)


def create_synthetic_decimal_schema(conn):
    """Create isolated test tables with TEXT price columns."""

    _require_synthetic_connection(conn)

    if conn.execute(
        "SELECT COUNT(*) FROM main.sqlite_master"
    ).fetchone()[0]:
        raise SyntheticDecimalWriteRejected(
            "Existing schema objects prohibited"
        )

    try:
        conn.execute("BEGIN IMMEDIATE")

        for sql in _TABLE_SQL.values():
            conn.execute(sql)
        _validate_decimal_schema(conn)
        conn.commit()

    except BaseException:
        conn.rollback()
        raise


def insert_synthetic_decimal_pair(conn, pair):
    """Atomically insert one exact-Decimal synthetic price pair."""

    if type(pair) is not DecimalPricePair:
        raise SyntheticDecimalWriteRejected(
            "DecimalPricePair required"
        )

    values = (
        pair.open_price,
        pair.high_price,
        pair.low_price,
        pair.close_price,
        pair.volume,
    )

    encoded = tuple(_exact_text(value) for value in values)

    opening, high, low, close, volume = values

    if any(value <= 0 for value in (opening, high, low, close)):
        raise SyntheticDecimalWriteRejected(
            "Nonpositive OHLC price"
        )

    if volume < 0:
        raise SyntheticDecimalWriteRejected("Negative volume")

    if not (
        low <= opening <= high
        and low <= close <= high
    ):
        raise SyntheticDecimalWriteRejected(
            "Invalid OHLC range"
        )

    if (
        not isinstance(pair.ticker, str)
        or not pair.ticker.strip()
        or pair.ticker != pair.ticker.strip()
    ):
        raise SyntheticDecimalWriteRejected("Invalid ticker")

    from datetime import date

    if not isinstance(pair.observation_date, str):
        raise SyntheticDecimalWriteRejected("Invalid date")

    try:
        parsed_date = date.fromisoformat(pair.observation_date)
    except ValueError as exc:
        raise SyntheticDecimalWriteRejected("Invalid date") from exc

    if parsed_date.isoformat() != pair.observation_date:
        raise SyntheticDecimalWriteRejected("Noncanonical date")

    _require_synthetic_connection(conn)

    try:
        conn.execute("BEGIN IMMEDIATE")
        _validate_decimal_schema(conn)

        conn.execute(
            """
            INSERT INTO synthetic_decimal_prices
                (ticker, date, close_price)
            VALUES (?, ?, ?)
            """,
            (
                pair.ticker,
                pair.observation_date,
                encoded[3],
            ),
        )

        conn.execute(
            """
            INSERT INTO synthetic_decimal_ohlcv
                (ticker, date, open_price, high_price,
                 low_price, close_price, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                pair.ticker,
                pair.observation_date,
                encoded[0],
                encoded[1],
                encoded[2],
                encoded[3],
                encoded[4],
            ),
        )

        conn.commit()

    except BaseException:
        conn.rollback()
        raise
