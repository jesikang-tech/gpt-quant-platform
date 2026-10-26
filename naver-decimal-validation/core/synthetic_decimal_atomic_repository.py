"""Synthetic-only atomic Decimal price storage.

Only caller-owned isolated SQLite memory databases are accepted.
No operational database connections, provider calls, or authorization.
Decimal values are stored as exact canonical text.
"""

from decimal import Decimal, InvalidOperation

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


def _validate_decimal_pair(pair):
    """Validate one synthetic Decimal pair and encode exact values."""
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

    return encoded


def insert_synthetic_decimal_pair(conn, pair):
    """Atomically insert one exact-Decimal synthetic price pair."""

    encoded = _validate_decimal_pair(pair)

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


def insert_synthetic_rebuild_batch(conn, requests, *, expected_keys, synthetic_fixture):
    """Store a fully prepared synthetic batch in caller-owned memory storage.

    Return its evidence-bound result only after the atomic insert commits.
    Evidence and revisions remain in that result, not in the SQLite tables.
    This grants no real-data persistence or operational rebuild authority.
    """
    if synthetic_fixture is not True:
        raise ValueError("Explicit synthetic fixture declaration required")

    from price_rebuild_adapter import prepare_synthetic_rebuild_batch
    from core.naver_decimal_price_pipeline import prepare_naver_decimal_price_pair

    batch = prepare_synthetic_rebuild_batch(
        requests, expected_keys=expected_keys, synthetic_fixture=synthetic_fixture,
    )
    pairs = tuple(
        prepare_naver_decimal_price_pair(
            bound.observation.ticker,
            bound.observation.observation_date,
            dict(zip(("Open", "High", "Low", "Close", "Volume"),
                     bound.rows.ohlcv_row[2:])),
            adjustment=bound.adjustment,
        )
        for bound in batch.pairs
    )
    insert_synthetic_decimal_batch(conn, pairs)
    return batch


def insert_synthetic_decimal_batch(conn, pairs):
    """Atomically insert a complete synthetic Decimal price batch.

    Only a caller-owned isolated in-memory SQLite database is permitted.
    All pairs are validated before any database write.
    """

    if type(pairs) not in (tuple, list) or not pairs:
        raise SyntheticDecimalWriteRejected(
            "Nonempty explicit synthetic batch required"
        )

    validated = []
    seen = set()

    for pair in pairs:
        encoded = _validate_decimal_pair(pair)

        key = (pair.ticker, pair.observation_date)

        if key in seen:
            raise SyntheticDecimalWriteRejected(
                "Duplicate synthetic batch key"
            )

        seen.add(key)
        validated.append((key, encoded))

    _require_synthetic_connection(conn)

    try:
        conn.execute("BEGIN IMMEDIATE")
        _validate_decimal_schema(conn)

        for (ticker, observation_date), encoded in validated:
            conn.execute(
                """
                INSERT INTO synthetic_decimal_prices
                    (ticker, date, close_price)
                VALUES (?, ?, ?)
                """,
                (ticker, observation_date, encoded[3]),
            )

            conn.execute(
                """
                INSERT INTO synthetic_decimal_ohlcv
                    (ticker, date, open_price, high_price,
                     low_price, close_price, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    ticker,
                    observation_date,
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


def _read_decimal_text(value):
    if type(value) is not str:
        raise SyntheticDecimalWriteRejected("Decimal TEXT required")
    try:
        number = Decimal(value)
    except InvalidOperation as exc:
        raise SyntheticDecimalWriteRejected("Malformed Decimal TEXT") from exc
    if not number.is_finite() or str(number) != value:
        raise SyntheticDecimalWriteRejected("Finite canonical Decimal TEXT required")
    return number


def read_synthetic_replay_prices(conn, *, ticker, analysis_date):
    """Read validated synthetic (date, Decimal close) tuples, never authority.

    Validate every stored pair for the requested ticker, including future
    rows, before applying the inclusive analysis-date cutoff. Other tickers
    are outside this read's scope. An absent ticker or empty as-of window
    returns (). Source evidence, adjustment and revisions are not stored in
    these tables and cannot be reconstructed or authenticated by this read.
    No connection is opened and no transaction or data is changed.
    """
    from datetime import date
    from price_rebuild_adapter import (
        SyntheticRebuildRows,
        prepare_synthetic_replay_asof_prices,
    )

    if type(ticker) is not str or not ticker or ticker != ticker.strip():
        raise ValueError("Canonical ticker required")
    if type(analysis_date) is not str:
        raise ValueError("Canonical analysis date required")
    try:
        parsed_date = date.fromisoformat(analysis_date)
    except ValueError as exc:
        raise ValueError("Canonical analysis date required") from exc
    if parsed_date.isoformat() != analysis_date:
        raise ValueError("Canonical analysis date required")

    _require_synthetic_connection(conn)
    _validate_decimal_schema(conn)
    prices = conn.execute(
        "SELECT ticker, date, close_price FROM main.synthetic_decimal_prices "
        "WHERE ticker = ? ORDER BY date", (ticker,),
    ).fetchall()
    ohlcv = conn.execute(
        "SELECT ticker, date, open_price, high_price, low_price, close_price, volume "
        "FROM main.synthetic_decimal_ohlcv WHERE ticker = ? ORDER BY date", (ticker,),
    ).fetchall()
    if [row[:2] for row in prices] != [row[:2] for row in ohlcv]:
        raise SyntheticDecimalWriteRejected("PRICE/OHLCV keys mismatch")

    rows = []
    for price_row, ohlcv_row in zip(prices, ohlcv):
        values = tuple(_read_decimal_text(value) for value in ohlcv_row[2:])
        pair = DecimalPricePair(ohlcv_row[0], ohlcv_row[1], *values)
        _validate_decimal_pair(pair)
        close = _read_decimal_text(price_row[2])
        if close != pair.close_price:
            raise SyntheticDecimalWriteRejected("PRICE/OHLCV close mismatch")
        if price_row[2] != ohlcv_row[5]:
            raise SyntheticDecimalWriteRejected("PRICE/OHLCV close TEXT mismatch")
        rows.append(SyntheticRebuildRows(
            ticker, (ticker, pair.observation_date, close),
            (ticker, pair.observation_date, *values),
        ))
    if not rows:
        return ()
    return prepare_synthetic_replay_asof_prices(tuple(rows), analysis_date)
