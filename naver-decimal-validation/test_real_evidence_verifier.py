"""Synthetic, offline tests for the local NAVER evidence verifier."""

from hashlib import sha256
import json

import pytest

from real_evidence_verifier import verify_evidence_directory, verify_selected_evidence_directory


TICKERS = ("005930", "035420", "000660", "005380")
NORMAL = "20260102|100|110|90|105|1000"
ZERO = "20260105|0|0|0|105|0"
ONE_UNIT = "20260106|100|104|90|105|1000"


def _make_evidence(tmp_path, rows=None):
    rows = rows or {
        "005930": (NORMAL, ZERO, ONE_UNIT),
        "035420": (NORMAL,),
        "000660": (NORMAL,),
        "005380": (NORMAL,),
    }
    manifest = []

    for ticker in TICKERS:
        body = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            "<protocol><chartdata>"
            + "".join(
                f'<item data="{row}" />' for row in rows[ticker]
            )
            + "</chartdata></protocol>"
        ).encode("utf-8")

        (tmp_path / f"{ticker}.xml").write_bytes(body)

        manifest.append({
            "ticker": ticker,
            "file": f"{ticker}.xml",
            "bytes": len(body),
            "sha256": sha256(body).hexdigest(),
            "provenance_verified": False,
            "adjustment": "UNKNOWN",
            "analysis_authorized": False,
            "persistence_authorized": False,
        })

    (tmp_path / "manifest.json").write_text(
        json.dumps(manifest), encoding="utf-8"
    )
    return manifest


def _save_manifest(tmp_path, manifest):
    (tmp_path / "manifest.json").write_text(
        json.dumps(manifest), encoding="utf-8"
    )


def test_four_ticker_classification(tmp_path):
    _make_evidence(tmp_path)
    result = verify_evidence_directory(tmp_path)

    assert len(result) == 4
    assert sum(row["rows"] for row in result) == 6
    assert sum(row["normal"] for row in result) == 4
    assert sum(row["zero_ohlc"] for row in result) == 1
    assert sum(row["one_unit"] for row in result) == 1


def test_changed_xml_bytes_are_rejected(tmp_path):
    _make_evidence(tmp_path)
    path = tmp_path / "005930.xml"
    path.write_bytes(path.read_bytes() + b" ")

    with pytest.raises(ValueError, match="Byte count mismatch"):
        verify_evidence_directory(tmp_path)


def test_wrong_sha256_is_rejected(tmp_path):
    manifest = _make_evidence(tmp_path)
    manifest[0]["sha256"] = "0" * 64
    _save_manifest(tmp_path, manifest)

    with pytest.raises(ValueError, match="SHA-256 mismatch"):
        verify_evidence_directory(tmp_path)


def test_wrong_byte_count_is_rejected(tmp_path):
    manifest = _make_evidence(tmp_path)
    manifest[0]["bytes"] += 1
    _save_manifest(tmp_path, manifest)

    with pytest.raises(ValueError, match="Byte count mismatch"):
        verify_evidence_directory(tmp_path)


def test_duplicate_ticker_is_rejected(tmp_path):
    manifest = _make_evidence(tmp_path)
    manifest[1]["ticker"] = manifest[0]["ticker"]
    _save_manifest(tmp_path, manifest)

    with pytest.raises(ValueError, match="Unexpected or duplicate"):
        verify_evidence_directory(tmp_path)


@pytest.mark.parametrize(
    "field,value",
    [
        ("provenance_verified", True),
        ("adjustment", "VERIFIED"),
        ("analysis_authorized", True),
        ("persistence_authorized", True),
    ],
)
def test_authority_escalation_is_rejected(tmp_path, field, value):
    manifest = _make_evidence(tmp_path)
    manifest[0][field] = value
    _save_manifest(tmp_path, manifest)

    with pytest.raises(ValueError, match="Unsafe authorization"):
        verify_evidence_directory(tmp_path)


def test_invalid_ohlcv_is_rejected(tmp_path):
    rows = {ticker: (NORMAL,) for ticker in TICKERS}
    rows["005930"] = ("20260102|100|90|95|105|1000",)
    _make_evidence(tmp_path, rows)

    with pytest.raises(ValueError, match="Invalid NAVER OHLCV"):
        verify_evidence_directory(tmp_path)

def test_selected_evidence_four_tickers_match_existing_verifier(tmp_path):
    from real_evidence_verifier import verify_selected_evidence_directory

    _make_evidence(tmp_path)

    existing = verify_evidence_directory(tmp_path)
    selected = verify_selected_evidence_directory(
        tmp_path, tuple(reversed(TICKERS))
    )

    assert {item["ticker"]: item for item in selected} == {
        item["ticker"]: item for item in existing
    }
    assert tuple(item["ticker"] for item in selected) == tuple(sorted(TICKERS))


def test_selected_evidence_rejects_incomplete_expected_coverage(tmp_path):
    from real_evidence_verifier import verify_selected_evidence_directory

    _make_evidence(tmp_path)

    with pytest.raises(ValueError, match="coverage"):
        verify_selected_evidence_directory(tmp_path, ("005930",))


@pytest.mark.parametrize(
    "tickers",
    [
        (),
        ("005930", "005930"),
        ("../bad",),
        ("00593A",),
        ("005930.xml",),
        ["005930"],
    ],
)
def test_selected_evidence_rejects_invalid_ticker_contract(tmp_path, tickers):
    from real_evidence_verifier import verify_selected_evidence_directory

    with pytest.raises(ValueError):
        verify_selected_evidence_directory(tmp_path, tickers)


def test_selected_evidence_rejects_modified_xml(tmp_path):
    from real_evidence_verifier import verify_selected_evidence_directory

    _make_evidence(tmp_path)
    path = tmp_path / "005930.xml"
    path.write_bytes(path.read_bytes() + b"modified")

    with pytest.raises(ValueError, match="Byte count mismatch"):
        verify_selected_evidence_directory(tmp_path, TICKERS)


def test_selected_evidence_rejects_authority_escalation(tmp_path):
    from real_evidence_verifier import verify_selected_evidence_directory

    manifest = _make_evidence(tmp_path)
    manifest[0]["provenance_verified"] = True
    _save_manifest(tmp_path, manifest)

    with pytest.raises(ValueError, match="Unsafe authorization"):
        verify_selected_evidence_directory(tmp_path, TICKERS)

def test_selected_evidence_two_tickers_success(tmp_path):
    from real_evidence_verifier import verify_selected_evidence_directory

    manifest = _make_evidence(tmp_path)
    selected = ("005930", "035420")

    _save_manifest(
        tmp_path,
        [record for record in manifest if record["ticker"] in selected],
    )

    result = verify_selected_evidence_directory(tmp_path, selected)

    assert tuple(item["ticker"] for item in result) == selected
    assert all(item["rows"] > 0 for item in result)
    assert all(len(item["sha256"]) == 64 for item in result)



@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("bytes", True),
        ("bytes", "123"),
        ("bytes", None),
        ("sha256", 123),
        ("sha256", None),
    ],
)
@pytest.mark.parametrize(
    "verifier",
    [
        verify_evidence_directory,
        verify_selected_evidence_directory,
    ],
)
def test_invalid_manifest_metadata_types_are_rejected(
    tmp_path, field, value, verifier
):
    manifest = _make_evidence(tmp_path)
    manifest[0][field] = value
    _save_manifest(tmp_path, manifest)

    with pytest.raises(ValueError):
        if verifier is verify_selected_evidence_directory:
            verifier(tmp_path, TICKERS)
        else:
            verifier(tmp_path)
