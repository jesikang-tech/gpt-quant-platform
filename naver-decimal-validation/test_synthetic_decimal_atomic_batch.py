"""Synthetic-only Decimal batch atomicity regression tests."""

import sqlite3
from decimal import Decimal

import pytest

from core.decimal_synthetic_bridge import DecimalPricePair
from core.synthetic_atomic_price_repository import SyntheticPriceWriteRejected
from core.synthetic_decimal_atomic_repository import (
    SyntheticDecimalWriteRejected,
    create_synthetic_decimal_schema,
    insert_synthetic_decimal_batch,
    insert_synthetic_decimal_pair,
    insert_synthetic_rebuild_batch,
)


def _pair(ticker, day, close="10.12345678901234567890"):
    return DecimalPricePair(
        ticker=ticker,
        observation_date=day,
        open_price=Decimal("10"),
        high_price=Decimal("11"),
        low_price=Decimal("9"),
        close_price=Decimal(close),
        volume=Decimal("100"),
    )


def _database():
    conn = sqlite3.connect(":memory:")
    create_synthetic_decimal_schema(conn)
    return conn


def _rows(conn, table):
    return conn.execute(
        f"SELECT * FROM {table} ORDER BY ticker, date"
    ).fetchall()


def test_batch_stores_multiple_pairs_atomically_with_exact_decimal():
    conn = _database()
    try:
        insert_synthetic_decimal_batch(
            conn,
            [
                _pair("AAA", "2026-01-02"),
                _pair("BBB", "2026-01-05"),
            ],
        )

        prices = _rows(conn, "synthetic_decimal_prices")
        ohlcv = _rows(conn, "synthetic_decimal_ohlcv")

        assert len(prices) == len(ohlcv) == 2
        assert prices[0][2] == "10.12345678901234567890"
        assert ohlcv[0][5] == prices[0][2]
        assert ohlcv[1][5] == prices[1][2]
        assert not conn.in_transaction
    finally:
        conn.close()


def test_duplicate_input_key_rejected_without_writes():
    conn = _database()
    try:
        pair = _pair("AAA", "2026-01-02")

        with pytest.raises(
            SyntheticDecimalWriteRejected,
            match="Duplicate synthetic batch key",
        ):
            insert_synthetic_decimal_batch(conn, [pair, pair])

        assert _rows(conn, "synthetic_decimal_prices") == []
        assert _rows(conn, "synthetic_decimal_ohlcv") == []
    finally:
        conn.close()


def test_existing_database_key_failure_rolls_back_entire_batch():
    conn = _database()
    try:
        insert_synthetic_decimal_pair(
            conn, _pair("BBB", "2026-01-05")
        )

        before_prices = _rows(conn, "synthetic_decimal_prices")
        before_ohlcv = _rows(conn, "synthetic_decimal_ohlcv")

        with pytest.raises(sqlite3.IntegrityError):
            insert_synthetic_decimal_batch(
                conn,
                [
                    _pair("AAA", "2026-01-02"),
                    _pair("BBB", "2026-01-05"),
                ],
            )

        assert _rows(conn, "synthetic_decimal_prices") == before_prices
        assert _rows(conn, "synthetic_decimal_ohlcv") == before_ohlcv
        assert not conn.in_transaction
    finally:
        conn.close()


def test_later_invalid_pair_rejected_before_any_write():
    conn = _database()
    try:
        invalid = _pair("BBB", "2026-01-05", close="12")

        with pytest.raises(
            SyntheticDecimalWriteRejected,
            match="Invalid OHLC range",
        ):
            insert_synthetic_decimal_batch(
                conn,
                [_pair("AAA", "2026-01-02"), invalid],
            )

        assert _rows(conn, "synthetic_decimal_prices") == []
        assert _rows(conn, "synthetic_decimal_ohlcv") == []
    finally:
        conn.close()


@pytest.mark.parametrize("pairs", [[], (), None, {}])
def test_empty_or_unsupported_batch_rejected(pairs):
    conn = _database()
    try:
        with pytest.raises(
            SyntheticDecimalWriteRejected,
            match="Nonempty explicit synthetic batch required",
        ):
            insert_synthetic_decimal_batch(conn, pairs)

        assert _rows(conn, "synthetic_decimal_prices") == []
    finally:
        conn.close()


def test_file_backed_database_is_rejected(tmp_path):
    conn = sqlite3.connect(tmp_path / "synthetic.db")
    try:
        with pytest.raises(SyntheticPriceWriteRejected):
            insert_synthetic_decimal_batch(
                conn, [_pair("AAA", "2026-01-02")]
            )
    finally:
        conn.close()
def test_later_ohlcv_insert_failure_rolls_back_whole_batch():
    conn = _database()
    try:
        # Seed only OHLCV for the later key. Its PRICE insert can succeed,
        # but its OHLCV insert must fail on the existing primary key.
        later = _pair("BBB", "2026-01-05")
        conn.execute(
            "INSERT INTO synthetic_decimal_ohlcv VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                later.ticker,
                later.observation_date,
                "10",
                "11",
                "9",
                str(later.close_price),
                "100",
            ),
        )
        conn.commit()

        before_prices = _rows(conn, "synthetic_decimal_prices")
        before_ohlcv = _rows(conn, "synthetic_decimal_ohlcv")

        with pytest.raises(sqlite3.IntegrityError):
            insert_synthetic_decimal_batch(
                conn,
                [
                    _pair("AAA", "2026-01-02"),
                    later,
                ],
            )

        assert _rows(conn, "synthetic_decimal_prices") == before_prices
        assert _rows(conn, "synthetic_decimal_ohlcv") == before_ohlcv
        assert not conn.in_transaction
    finally:
        conn.close()


def test_existing_transaction_is_rejected_without_rollback():
    conn = _database()
    try:
        conn.execute("BEGIN")
        assert conn.in_transaction

        with pytest.raises(
            SyntheticPriceWriteRejected,
            match="Existing transaction prohibited",
        ):
            insert_synthetic_decimal_batch(
                conn,
                [_pair("AAA", "2026-01-02")],
            )

        # The caller's transaction remains under caller ownership.
        assert conn.in_transaction
        conn.rollback()

        assert _rows(conn, "synthetic_decimal_prices") == []
        assert _rows(conn, "synthetic_decimal_ohlcv") == []
    finally:
        conn.close()


def _rebuild_request(ticker, day, revision=None):
    from hashlib import sha256
    from core.naver_source_evidence import (
        AcquisitionContext, ClaimedProvider, EvidenceReference,
        NaverSourceEvidence, ObservationIdentity,
    )
    from price_rebuild_adapter import SyntheticRebuildRequest

    row = (f"{day.replace('-', '')}|100000000000000000000|110000000000000000000|"
           "90000000000000000000|105000000000000000001|1000")
    raw = f'<protocol><chartdata><item data="{row}" /></chartdata></protocol>'.encode()
    digest = sha256(raw).hexdigest()
    identity = ObservationIdentity(ticker, day, digest)
    evidence = NaverSourceEvidence(
        ClaimedProvider("NAVER"),
        AcquisitionContext("SYNTHETIC_FIXTURE", "2026-01-06T00:00:00Z", "synthetic://response"),
        identity,
        (EvidenceReference("fixture", "SYNTHETIC_RESPONSE", "NAVER", "TEST_ONLY",
                           "synthetic://response", digest),),
    )
    return SyntheticRebuildRequest(raw, evidence, identity, "UNADJUSTED", revision)


def _integration_requests():
    return (_rebuild_request("BBB", "2026-01-05", "revision-b"),
            _rebuild_request("AAA", "2026-01-02"))


def _integration_keys(requests):
    return [(r.expected_observation.ticker, r.expected_observation.observation_date)
            for r in requests]


def test_rebuild_integration_stores_exact_values_and_preserves_evidence(monkeypatch):
    from core import synthetic_decimal_atomic_repository as storage

    requests = _integration_requests()
    conn = _database()
    calls = []
    original = storage.insert_synthetic_decimal_batch

    def recording_insert(connection, pairs):
        assert type(pairs) is tuple and len(pairs) == 2
        assert not connection.in_transaction
        calls.append(pairs)
        return original(connection, pairs)

    try:
        with monkeypatch.context() as patch:
            patch.setattr(storage, "insert_synthetic_decimal_batch", recording_insert)
            result = insert_synthetic_rebuild_batch(
                conn, requests, expected_keys=_integration_keys(requests), synthetic_fixture=True,
            )
        assert len(calls) == 1
        assert not conn.in_transaction
        assert _rows(conn, "synthetic_decimal_prices") == [
            ("AAA", "2026-01-02", "105000000000000000001"),
            ("BBB", "2026-01-05", "105000000000000000001"),
        ]
        assert _rows(conn, "synthetic_decimal_ohlcv") == [
            (ticker, day, "100000000000000000000", "110000000000000000000",
             "90000000000000000000", "105000000000000000001", "1000")
            for ticker, day in sorted(_integration_keys(requests))
        ]
        assert result.verification_status == "SYNTHETIC_ONLY"
        assert result.coverage.status == "COMPLETE_UNVERIFIED"
        for bound, request in zip(result.pairs, reversed(requests)):
            assert bound.evidence is request.evidence
            assert bound.observation is request.expected_observation
            assert bound.source_sha256 == request.expected_observation.content_sha256
            assert bound.revision_id == request.revision_id
            assert bound.adjustment == request.adjustment
        for item in (result, result.coverage, *result.pairs):
            for field in ("provenance_verified", "analysis_authorized", "persistence_authorized",
                          "rebuild_authorized", "execution_authorized"):
                assert getattr(item, field) is False
    finally:
        conn.close()


@pytest.mark.parametrize("failure", ["later_request", "coverage"])
def test_rebuild_integration_preparation_failure_never_calls_storage(monkeypatch, failure):
    from dataclasses import replace
    from core import synthetic_decimal_atomic_repository as storage

    requests = _integration_requests()
    expected = _integration_keys(requests)
    if failure == "later_request":
        requests = (requests[0], replace(requests[1], raw_response=requests[1].raw_response + b" "))
        message = "SHA-256 mismatch"
    else:
        expected = expected[:1]
        message = "Incomplete synthetic rebuild coverage"
    calls = []

    def forbidden_insert(*args, **kwargs):
        calls.append(True)
        raise AssertionError("Persistence must not start")

    conn = _database()
    try:
        with monkeypatch.context() as patch:
            patch.setattr(storage, "insert_synthetic_decimal_batch", forbidden_insert)
            with pytest.raises(ValueError, match=message):
                insert_synthetic_rebuild_batch(
                    conn, requests, expected_keys=expected, synthetic_fixture=True,
                )
        assert calls == []
        assert _rows(conn, "synthetic_decimal_prices") == []
        assert _rows(conn, "synthetic_decimal_ohlcv") == []
    finally:
        conn.close()


def test_rebuild_integration_later_ohlcv_collision_rolls_back():
    requests = _integration_requests()
    conn = _database()
    try:
        conn.execute("INSERT INTO synthetic_decimal_ohlcv VALUES (?, ?, ?, ?, ?, ?, ?)",
                     ("BBB", "2026-01-05", "10", "11", "9", "10", "100"))
        conn.commit()
        before = _rows(conn, "synthetic_decimal_ohlcv")
        with pytest.raises(sqlite3.IntegrityError):
            insert_synthetic_rebuild_batch(
                conn, requests, expected_keys=_integration_keys(requests), synthetic_fixture=True,
            )
        assert _rows(conn, "synthetic_decimal_prices") == []
        assert _rows(conn, "synthetic_decimal_ohlcv") == before
        assert not conn.in_transaction
    finally:
        conn.close()


@pytest.mark.parametrize("connection_kind", ["file", "transaction"])
def test_rebuild_integration_preserves_connection_rejections(tmp_path, connection_kind):
    requests = _integration_requests()
    conn = sqlite3.connect(tmp_path / "integration.sqlite3") if connection_kind == "file" else _database()
    try:
        if connection_kind == "transaction":
            conn.execute("BEGIN")
        with pytest.raises(SyntheticPriceWriteRejected):
            insert_synthetic_rebuild_batch(
                conn, requests, expected_keys=_integration_keys(requests), synthetic_fixture=True,
            )
        if connection_kind == "transaction":
            assert conn.in_transaction
            conn.rollback()
            assert _rows(conn, "synthetic_decimal_prices") == []
            assert _rows(conn, "synthetic_decimal_ohlcv") == []
        else:
            assert conn.execute("SELECT name FROM sqlite_master").fetchall() == []
    finally:
        conn.close()


@pytest.mark.parametrize("declaration", [False, None, 1, "True"])
def test_rebuild_integration_requires_exact_synthetic_declaration(declaration):
    with pytest.raises(ValueError, match="Explicit synthetic fixture"):
        insert_synthetic_rebuild_batch(
            None, (), expected_keys=(), synthetic_fixture=declaration,
        )


def test_rebuild_integration_success_cannot_authorize_real_persistence():
    from core.naver_persistence_entry import persist_naver_observation
    from core.price_provenance_gate import PriceProvenanceRejected
    from price_rebuild_adapter import prepare_real_rebuild_rows

    requests = _integration_requests()
    conn = _database()
    calls = []
    try:
        result = insert_synthetic_rebuild_batch(
            conn, requests, expected_keys=_integration_keys(requests), synthetic_fixture=True,
        )
        before = (_rows(conn, "synthetic_decimal_prices"), _rows(conn, "synthetic_decimal_ohlcv"))
        with pytest.raises(ValueError, match="RebuildPreflight required"):
            prepare_real_rebuild_rows(result)
        with pytest.raises(PriceProvenanceRejected, match="persistence is prohibited"):
            persist_naver_observation(result, lambda value: calls.append(value))
        assert calls == []
        assert (_rows(conn, "synthetic_decimal_prices"), _rows(conn, "synthetic_decimal_ohlcv")) == before
    finally:
        conn.close()


def test_rebuild_integration_retry_after_success_preserves_exact_rows():
    requests = _integration_requests()
    expected_keys = _integration_keys(requests)
    tables = ("synthetic_decimal_prices", "synthetic_decimal_ohlcv")
    conn = _database()
    try:
        insert_synthetic_rebuild_batch(
            conn, requests, expected_keys=expected_keys, synthetic_fixture=True,
        )
        before = tuple(
            tuple(tuple(value.encode("utf-8") for value in row) for row in _rows(conn, table))
            for table in tables
        )
        assert all(len(rows) == 2 for rows in before)
        assert not conn.in_transaction
        with pytest.raises(sqlite3.IntegrityError, match="UNIQUE constraint failed"):
            insert_synthetic_rebuild_batch(
                conn, requests, expected_keys=expected_keys, synthetic_fixture=True,
            )
        after = tuple(
            tuple(tuple(value.encode("utf-8") for value in row) for row in _rows(conn, table))
            for table in tables
        )
        assert after == before
        assert not conn.in_transaction
    finally:
        conn.close()


def test_rebuild_integration_retry_after_collision_removal_stores_complete_batch():
    requests = _integration_requests()
    expected_keys = _integration_keys(requests)
    later_key = sorted(expected_keys)[-1]
    conn = _database()
    try:
        conn.execute("INSERT INTO synthetic_decimal_ohlcv VALUES (?, ?, ?, ?, ?, ?, ?)",
                     (*later_key, "10", "11", "9", "10", "100"))
        conn.commit()
        before = _rows(conn, "synthetic_decimal_ohlcv")
        with pytest.raises(sqlite3.IntegrityError, match="UNIQUE constraint failed"):
            insert_synthetic_rebuild_batch(
                conn, requests, expected_keys=expected_keys, synthetic_fixture=True,
            )
        assert _rows(conn, "synthetic_decimal_prices") == []
        assert _rows(conn, "synthetic_decimal_ohlcv") == before
        assert not conn.in_transaction

        conn.execute("DELETE FROM synthetic_decimal_ohlcv WHERE ticker = ? AND date = ?", later_key)
        conn.commit()
        assert _rows(conn, "synthetic_decimal_ohlcv") == []
        insert_synthetic_rebuild_batch(
            conn, requests, expected_keys=expected_keys, synthetic_fixture=True,
        )
        assert _rows(conn, "synthetic_decimal_prices") == [
            (ticker, day, "105000000000000000001") for ticker, day in sorted(expected_keys)
        ]
        assert _rows(conn, "synthetic_decimal_ohlcv") == [
            (ticker, day, "100000000000000000000", "110000000000000000000",
             "90000000000000000000", "105000000000000000001", "1000")
            for ticker, day in sorted(expected_keys)
        ]
        assert not conn.in_transaction
    finally:
        conn.close()
