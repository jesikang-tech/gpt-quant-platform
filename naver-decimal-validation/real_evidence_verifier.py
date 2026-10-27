"""Offline verification of explicitly supplied NAVER evidence files.

This module does not fetch data, access databases, authenticate a source,
or authorize analysis/persistence. Raw response files remain local.
"""

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

from price_rebuild_preflight import assess_rebuild_candidates
from core.naver_raw_observation import NaverRawObservation
from core.naver_http_response_validation import (
    NaverHighBelowCloseByOneRow,
    NaverZeroOhlcSpecialRow,
    validate_naver_http_response,
)


EXPECTED_TICKERS = frozenset({"005930", "035420", "000660", "005380"})


def verify_evidence_directory(directory):
    """Verify an explicit directory and return classification summaries."""
    directory = Path(directory)
    manifest_path = directory / "manifest.json"

    manifest = json.loads(manifest_path.read_bytes())
    if not isinstance(manifest, list) or len(manifest) != 4:
        raise ValueError("Expected four manifest records")

    tickers = [record["ticker"] for record in manifest]
    if set(tickers) != EXPECTED_TICKERS or len(set(tickers)) != 4:
        raise ValueError("Unexpected or duplicate tickers")

    summaries = []

    for record in manifest:
        ticker = record["ticker"]
        filename = f"{ticker}.xml"

        if record["file"] != filename:
            raise ValueError(f"Unexpected filename: {ticker}")

        if (
            record["provenance_verified"] is not False
            or record["adjustment"] != "UNKNOWN"
            or record["analysis_authorized"] is not False
            or record["persistence_authorized"] is not False
        ):
            raise ValueError(f"Unsafe authorization: {ticker}")

        raw = (directory / filename).read_bytes()

        if len(raw) != record["bytes"]:
            raise ValueError(f"Byte count mismatch: {ticker}")

        digest = sha256(raw).hexdigest()
        if digest != record["sha256"]:
            raise ValueError(f"SHA-256 mismatch: {ticker}")

        observations = validate_naver_http_response(
            raw, record["sha256"], ticker
        )

        counts = Counter(type(item) for item in observations)

        normal = counts.pop(NaverRawObservation, 0)
        zero = counts.pop(NaverZeroOhlcSpecialRow, 0)
        one_unit = counts.pop(NaverHighBelowCloseByOneRow, 0)

        if counts:
            raise ValueError(f"Unexpected observation types: {ticker}")

        for item in observations:
            if (
                item.provenance_verified is not False
                or item.adjustment != "UNKNOWN"
                or item.persistence_authorized is not False
            ):
                raise ValueError(f"Unexpected authority: {ticker}")

            if type(item) is NaverRawObservation:
                if hasattr(item, "analysis_authorized"):
                    raise ValueError(
                        f"Unexpected raw analysis authority: {ticker}"
                    )
            elif item.analysis_authorized is not False:
                raise ValueError(
                    f"Unexpected special-row authority: {ticker}"
                )

        preflight = assess_rebuild_candidates(ticker, observations)

        if (
            preflight.total_rows != len(observations)
            or preflight.normal_rows != normal
            or preflight.zero_ohlc_rows != zero
            or preflight.high_below_close_rows != one_unit
            or preflight.price_candidates != normal
            or preflight.ohlcv_candidates != normal
            or preflight.verification_status != "UNVERIFIED"
            or preflight.persistence_authorized is not False
        ):
            raise ValueError(f"Rebuild preflight mismatch: {ticker}")

        summaries.append({
            "ticker": ticker,
            "rows": len(observations),
            "normal": normal,
            "zero_ohlc": zero,
            "one_unit": one_unit,
            "sha256": digest,
        })

    return tuple(summaries)

def verify_selected_evidence_directory(directory, expected_tickers):
    """Verify an explicit synthetic/offline ticker set without granting authority."""
    if type(expected_tickers) not in (tuple, frozenset):
        raise ValueError("Expected immutable ticker collection")
    if not expected_tickers:
        raise ValueError("Expected nonempty ticker collection")
    if any(
        type(ticker) is not str
        or len(ticker) != 6
        or not ticker.isascii()
        or not ticker.isdecimal()
        for ticker in expected_tickers
    ):
        raise ValueError("Invalid ticker")
    if len(set(expected_tickers)) != len(expected_tickers):
        raise ValueError("Duplicate expected ticker")

    directory = Path(directory)
    manifest = json.loads((directory / "manifest.json").read_bytes())

    if type(manifest) is not list:
        raise ValueError("Malformed manifest")
    if len(manifest) != len(expected_tickers):
        raise ValueError("Manifest coverage mismatch")

    records = {}
    for record in manifest:
        if type(record) is not dict:
            raise ValueError("Malformed manifest record")
        ticker = record.get("ticker")
        if type(ticker) is not str or ticker not in expected_tickers:
            raise ValueError("Unexpected ticker")
        if ticker in records:
            raise ValueError("Duplicate manifest ticker")
        records[ticker] = record

    if set(records) != set(expected_tickers):
        raise ValueError("Incomplete manifest coverage")

    summaries = []
    for ticker in sorted(records):
        record = records[ticker]
        filename = ticker + ".xml"

        if record.get("file") != filename:
            raise ValueError("Unexpected filename")
        if (
            record.get("provenance_verified") is not False
            or record.get("adjustment") != "UNKNOWN"
            or record.get("analysis_authorized") is not False
            or record.get("persistence_authorized") is not False
        ):
            raise ValueError("Unsafe authorization")

        raw = (directory / filename).read_bytes()
        if type(record.get("bytes")) is not int:
            raise ValueError("Invalid byte count")
        if len(raw) != record["bytes"]:
            raise ValueError("Byte count mismatch")

        digest = sha256(raw).hexdigest()
        if type(record.get("sha256")) is not str:
            raise ValueError("Invalid digest")
        if digest != record["sha256"]:
            raise ValueError("SHA-256 mismatch")

        observations = validate_naver_http_response(
            raw, record["sha256"], ticker
        )
        counts = Counter(type(item) for item in observations)

        normal = counts.pop(NaverRawObservation, 0)
        zero = counts.pop(NaverZeroOhlcSpecialRow, 0)
        one_unit = counts.pop(NaverHighBelowCloseByOneRow, 0)

        if counts:
            raise ValueError("Unexpected observation type")

        for item in observations:
            if (
                item.provenance_verified is not False
                or item.adjustment != "UNKNOWN"
                or item.persistence_authorized is not False
            ):
                raise ValueError("Unexpected observation authority")
            if type(item) is NaverRawObservation:
                if hasattr(item, "analysis_authorized"):
                    raise ValueError("Unexpected raw analysis authority")
            elif item.analysis_authorized is not False:
                raise ValueError("Unexpected special-row authority")

        preflight = assess_rebuild_candidates(ticker, observations)
        if (
            preflight.total_rows != len(observations)
            or preflight.normal_rows != normal
            or preflight.zero_ohlc_rows != zero
            or preflight.high_below_close_rows != one_unit
            or preflight.price_candidates != normal
            or preflight.ohlcv_candidates != normal
            or preflight.verification_status != "UNVERIFIED"
            or preflight.persistence_authorized is not False
        ):
            raise ValueError("Rebuild preflight mismatch")

        summaries.append({
            "ticker": ticker,
            "rows": len(observations),
            "normal": normal,
            "zero_ohlc": zero,
            "one_unit": one_unit,
            "sha256": digest,
        })

    return tuple(summaries)
