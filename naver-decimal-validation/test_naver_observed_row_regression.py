"""Offline regression cases transcribed from NAVER XML observations.

These rows were previously observed in HTTP responses, but this test
constructs synthetic XML envelopes. It does not authenticate provenance,
verify the original HTTP response bytes, or authorize analysis/storage.
"""

from hashlib import sha256

import pytest

from core.naver_http_response_validation import (
    NaverHighBelowCloseByOneRow,
    NaverZeroOhlcSpecialRow,
    validate_naver_http_response,
)


ONE_UNIT_CASES = (
    ("005930", "20150127|27500|27999|27480|28000|199144"),
    ("005930", "20150217|27479|27539|27280|27540|114900"),
    ("005930", "20161024|31860|32159|31800|32160|185799"),
    ("035420", "20140923|154017|167035|153616|167036|347351"),
    ("035420", "20141222|148810|149210|146406|149211|45345"),
    ("035420", "20150123|155219|156220|152214|156221|99297"),
    ("035420", "20150320|128781|130984|128781|130985|90524"),
    ("035420", "20150623|127179|128180|125977|128181|46207"),
)

ZERO_OHLC_CASES = (
    ("005930", "20180430|0|0|0|53000|0"),
    ("005930", "20180502|0|0|0|53000|0"),
    ("005930", "20180503|0|0|0|53000|0"),
)


def _classify(ticker, raw_row):
    body = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<protocol><chartdata>'
        f'<item data="{raw_row}" />'
        '</chartdata></protocol>'
    ).encode("utf-8")

    result = validate_naver_http_response(
        body,
        sha256(body).hexdigest(),
        ticker,
    )

    assert len(result) == 1
    return result[0]


@pytest.mark.parametrize("ticker,raw_row", ONE_UNIT_CASES)
def test_observed_one_unit_case_remains_unverified_and_blocked(ticker, raw_row):
    evidence = _classify(ticker, raw_row)

    assert isinstance(evidence, NaverHighBelowCloseByOneRow)
    assert evidence.ticker == ticker
    assert evidence.raw_row == raw_row
    assert evidence.classification == "HIGH_BELOW_CLOSE_BY_ONE_UNVERIFIED"
    assert evidence.adjustment == "UNKNOWN"
    assert evidence.provenance_verified is False
    assert evidence.analysis_authorized is False
    assert evidence.persistence_authorized is False


@pytest.mark.parametrize("ticker,raw_row", ZERO_OHLC_CASES)
def test_observed_zero_ohlc_case_remains_unverified_and_blocked(ticker, raw_row):
    evidence = _classify(ticker, raw_row)

    assert isinstance(evidence, NaverZeroOhlcSpecialRow)
    assert evidence.ticker == ticker
    assert evidence.raw_row == raw_row
    assert evidence.classification == "ZERO_OHLC_NON_TRADING_EVIDENCE"
    assert evidence.adjustment == "UNKNOWN"
    assert evidence.provenance_verified is False
    assert evidence.analysis_authorized is False
    assert evidence.persistence_authorized is False
