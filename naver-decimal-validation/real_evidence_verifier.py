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