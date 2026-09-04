from unittest.mock import patch

from etf_analyzer import analyze_etf


def main():
    ticker = 'TEST001'
    prices = [10000, 10200, 10500, 10800, 11000, 11300, 11600]
    calls = []

    def fake_save(*args):
        calls.append(args)

    p1 = patch('etf_analyzer.save_or_update_etf_score', side_effect=fake_save)
    p2 = patch('etf_analyzer.save_score_history', side_effect=fake_save)
    p1.start()
    p2.start()
    try:
        result = analyze_etf(ticker, prices, '2026-09-01')
    finally:
        p2.stop()
        p1.stop()

    assert result['ticker'] == ticker
    assert len(calls) == 2
    assert all(call[-1] == '2026-09-01' for call in calls)

    print('=' * 40)
    print('ETF Analyzer Test')
    print('=' * 40)
    print(result)
    print('SAVE_CALLS=', calls)
    print('STATUS=PASS')


if __name__ == '__main__':
    main()