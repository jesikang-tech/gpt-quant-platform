import pytest
from price_test_support import isolated_price_db, phase8_test_scope


def test_etf_analysis_and_save_contract():
    ticker = 'TEST001'
    prices = [10000, 10200, 10500, 10800, 11000, 11300, 11600]
    # Keep the seven original anchors and 16% return, while meeting the
    # actual 60-observation eligibility requirement.
    anchors = prices
    prices = []
    for index, (left, right) in enumerate(zip(anchors, anchors[1:])):
        steps = 10 if index < 5 else 9
        prices.extend(left + (right - left) * step / steps for step in range(steps))
    prices.append(anchors[-1])
    calls = []

    def fake_save(*args):
        calls.append(args)

    with _scope.patches.context() as patches:
        patches.setattr(analyzer, 'save_or_update_etf_score', fake_save)
        patches.setattr(analyzer, 'save_score_history', fake_save)
        result = analyze_etf(ticker, prices, '2026-09-01')

    assert result['ticker'] == ticker
    assert len(calls) == 2
    assert all(call[-1] == '2026-09-01' for call in calls)

    assert len(prices) == 60
    assert result['return'] == pytest.approx(16.0)

    print('=' * 40)
    print('ETF Analyzer Test')
    print('=' * 40)
    print(result)
    print('SAVE_CALLS=', calls)
    print('STATUS=PASS')


def test_etf_analyzer_rejects_original_short_history():
    prices = [10000, 10200, 10500, 10800, 11000, 11300, 11600]
    calls = []
    with _scope.patches.context() as patches:
        patches.setattr(analyzer, 'save_or_update_etf_score', lambda *args: calls.append(args))
        patches.setattr(analyzer, 'save_score_history', lambda *args: calls.append(args))
        assert analyze_etf('TEST001', prices, '2026-09-01') is None
    assert calls == []


@pytest.fixture(autouse=True)
def _protected_flask_state(isolated_price_db, monkeypatch):
    with phase8_test_scope(isolated_price_db) as scope:
        import sys
        import etf_analyzer as analyzer
        target = sys.modules[__name__]
        for name, value in {"analyzer": analyzer, "analyze_etf": analyzer.analyze_etf,
                            "_scope": scope}.items():
            monkeypatch.setattr(target, name, value, raising=False)
        config_before = dict(scope.api.app.config)
        auth_path_before = scope.api.AUTH_CONFIG_PATH
        try:
            yield scope
        finally:
            scope.api.app.config.clear()
            scope.api.app.config.update(config_before)
            scope.api.AUTH_CONFIG_PATH = auth_path_before


if __name__ == '__main__':
    raise SystemExit('Run this protected contract with pytest.')
