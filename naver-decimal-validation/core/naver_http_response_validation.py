"""Offline validation for raw NAVER HTTP response bodies.

Transport success and content hashes provide integrity checks only.  They do
not authenticate NAVER provenance, adjustment status, or persistence safety.
"""

from dataclasses import dataclass, field
from hashlib import sha256
from hmac import compare_digest
from xml.etree import ElementTree

from core.naver_raw_observation import prepare_naver_raw_observation


class NaverHttpResponseRejected(ValueError):
    pass


@dataclass(frozen=True)
class NaverZeroOhlcSpecialRow:
    """Immutable evidence for NAVER's non-trading zero-OHLC row shape."""

    observation: object
    classification: str = field(
        default="ZERO_OHLC_NON_TRADING_EVIDENCE", init=False,
    )
    analysis_authorized: bool = field(default=False, init=False)
    persistence_authorized: bool = field(default=False, init=False)

    @property
    def ticker(self):
        return self.observation.ticker

    @property
    def observation_date(self):
        return self.observation.observation_date

    @property
    def raw_row(self):
        return self.observation.raw_row

    @property
    def values(self):
        return self.observation.values

    @property
    def provider(self):
        return self.observation.provider

    @property
    def adjustment(self):
        return self.observation.adjustment

    @property
    def provenance_verified(self):
        return self.observation.provenance_verified


def _local_name(element):
    return element.tag.rsplit("}", 1)[-1]


def _extract_raw_rows(root):
    if _local_name(root) != "protocol":
        raise NaverHttpResponseRejected("Invalid NAVER XML envelope")

    root_children = list(root)
    if len(root_children) != 1 or _local_name(root_children[0]) != "chartdata":
        raise NaverHttpResponseRejected("Invalid NAVER chartdata structure")

    chartdata = root_children[0]
    raw_rows = []
    for item in chartdata:
        if (
            _local_name(item) != "item"
            or set(item.attrib) != {"data"}
            or list(item)
            or (item.text is not None and item.text.strip())
        ):
            raise NaverHttpResponseRejected("Malformed NAVER item")
        raw_rows.append(item.attrib["data"])

    if not raw_rows:
        raise NaverHttpResponseRejected("NAVER XML contains no OHLCV rows")
    return raw_rows


def validate_naver_http_response(raw_response, expected_sha256, ticker):
    """Validate one raw XML response and return immutable observations.

    The digest is calculated directly from ``raw_response``.  No decoding or
    re-encoding occurs before the integrity check.
    """

    if type(raw_response) is not bytes:
        raise NaverHttpResponseRejected("Raw HTTP response must be bytes")

    if (
        type(expected_sha256) is not str
        or len(expected_sha256) != 64
        or any(character not in "0123456789abcdefABCDEF" for character in expected_sha256)
    ):
        raise NaverHttpResponseRejected("Invalid expected SHA-256")

    actual_sha256 = sha256(raw_response).hexdigest()
    if not compare_digest(actual_sha256, expected_sha256.lower()):
        raise NaverHttpResponseRejected("SHA-256 mismatch")

    try:
        root = ElementTree.fromstring(raw_response)
    except (ElementTree.ParseError, ValueError) as exc:
        raise NaverHttpResponseRejected("Malformed NAVER XML") from exc

    raw_rows = _extract_raw_rows(root)

    try:
        observations = tuple(
            prepare_naver_raw_observation(ticker, raw_row)
            for raw_row in raw_rows
        )
    except (TypeError, ValueError) as exc:
        raise NaverHttpResponseRejected("Invalid NAVER OHLCV row") from exc

    classified_observations = []
    for observation in observations:
        try:
            opening, high, low, close, volume = map(int, observation.values)
        except ValueError as exc:
            raise NaverHttpResponseRejected("Invalid NAVER OHLCV values") from exc

        is_special_row = (
            opening == 0
            and high == 0
            and low == 0
            and close > 0
            and volume == 0
        )
        is_normal_row = (
            min(opening, high, low, close) > 0
            and volume >= 0
            and high >= max(opening, close)
            and low <= min(opening, close)
        )

        if is_special_row:
            classified_observations.append(NaverZeroOhlcSpecialRow(observation))
        elif is_normal_row:
            classified_observations.append(observation)
        else:
            raise NaverHttpResponseRejected("Invalid NAVER OHLCV values")

    dates = tuple(observation.observation_date for observation in observations)
    if len(set(dates)) != len(dates):
        raise NaverHttpResponseRejected("Duplicate NAVER observation date")
    if any(earlier >= later for earlier, later in zip(dates, dates[1:])):
        raise NaverHttpResponseRejected("Unordered NAVER observation dates")

    return tuple(classified_observations)
