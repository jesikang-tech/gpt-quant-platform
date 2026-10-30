"""Offline tests for adjustment-request metadata; never authorize prices."""
from dataclasses import FrozenInstanceError

import pytest

from price_provider_validation.adjustment_request import (
    AdjustmentRequestDecision,
    assess_adjustment_request,
)
from price_provider_validation.provider_contract import (
    ProviderObservationRejected,
)


@pytest.mark.parametrize(
    "value,expected",
    [
        ("0", "ADJUSTED"),
        ("1", "UNADJUSTED"),
    ],
)
def test_documented_kis_request_values_remain_unverified(value, expected):
    decision = assess_adjustment_request(
        "KIS", "inquire_daily_itemchartprice", "FID_ORG_ADJ_PRC", value
    )

    assert decision.provider == "KIS"
    assert decision.requested_value == value
    assert decision.declared_request_policy == expected
    assert decision.response_adjustment == "UNKNOWN"
    assert decision.independently_verified is False
    assert decision.analysis_authorized is False
    assert decision.persistence_authorized is False


@pytest.mark.parametrize(
    "provider,api_id,parameter,value",
    [
        ("KIWOOM", "ka10081", "FID_ORG_ADJ_PRC", "0"),
        ("KIWOOM", "ka10086", "FID_ORG_ADJ_PRC", "1"),
        ("KIS", "inquire_daily_price", "FID_ORG_ADJ_PRC", "0"),
        ("KIS", "inquire_daily_itemchartprice", "INVALID", "0"),
        ("KIS", "inquire_daily_itemchartprice", "FID_ORG_ADJ_PRC", "2"),
        ("KIS", "inquire_daily_itemchartprice", "FID_ORG_ADJ_PRC", ""),
        ("KIS", "inquire_daily_itemchartprice", "FID_ORG_ADJ_PRC", 0),
        (None, "inquire_daily_itemchartprice", "FID_ORG_ADJ_PRC", "0"),
        ("KIS", None, "FID_ORG_ADJ_PRC", "0"),
        ("KIS", "inquire_daily_itemchartprice", None, "0"),
    ],
)
def test_unsupported_or_invalid_requests_rejected(
    provider, api_id, parameter, value
):
    with pytest.raises(ProviderObservationRejected):
        assess_adjustment_request(provider, api_id, parameter, value)


@pytest.mark.parametrize(
    "value,expected",
    [
        ("0", "UNADJUSTED"),
        ("1", "ADJUSTED"),
    ],
)
def test_kiwoom_ka10081_request_values_remain_unverified(value, expected):
    decision = assess_adjustment_request(
        "KIWOOM", "ka10081", "upd_stkpc_tp", value
    )

    assert decision.provider == "KIWOOM"
    assert decision.api_id == "ka10081"
    assert decision.parameter == "upd_stkpc_tp"
    assert decision.requested_value == value
    assert decision.declared_request_policy == expected
    assert decision.response_adjustment == "UNKNOWN"
    assert decision.independently_verified is False
    assert decision.analysis_authorized is False
    assert decision.persistence_authorized is False


@pytest.mark.parametrize(
    "parameter,value",
    [
        ("upd_stkpc_tp", "2"),
        ("upd_stkpc_tp", ""),
        ("upd_stkpc_tp", 0),
        ("FID_ORG_ADJ_PRC", "0"),
        ("invalid", "1"),
    ],
)
def test_kiwoom_ka10081_invalid_requests_rejected(parameter, value):
    with pytest.raises(ProviderObservationRejected):
        assess_adjustment_request(
            "KIWOOM", "ka10081", parameter, value
        )


def test_kiwoom_ka10086_adjustment_contract_remains_unavailable():
    with pytest.raises(ProviderObservationRejected):
        assess_adjustment_request(
            "KIWOOM", "ka10086", "upd_stkpc_tp", "1"
        )

def test_decision_is_frozen():
    decision = assess_adjustment_request(
        "KIS", "inquire_daily_itemchartprice", "FID_ORG_ADJ_PRC", "0"
    )

    with pytest.raises(FrozenInstanceError):
        decision.analysis_authorized = True


def test_no_default_authorization_even_when_directly_constructed():
    decision = AdjustmentRequestDecision(
        provider="KIS",
        api_id="inquire_daily_itemchartprice",
        parameter="FID_ORG_ADJ_PRC",
        requested_value="0",
        declared_request_policy="ADJUSTED",
    )

    assert decision.response_adjustment == "UNKNOWN"
    assert decision.independently_verified is False
    assert decision.analysis_authorized is False
    assert decision.persistence_authorized is False
