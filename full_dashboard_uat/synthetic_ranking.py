"""Synthetic ETF ranking response for isolated dashboard UAT.

No operating database, market-data provider or broker access.
All values are fictional browser-test fixtures.
"""

from flask import jsonify


_SYNTHETIC_ROWS = (
    {
        "ticker": "111111",
        "name": "UAT Synthetic ETF Alpha",
        "rank": 1,
        "score": 95,
        "enhanced_score": 95,
        "grade": "A",
        "prediction": "UPTREND",
        "stability": "HIGH",
        "return_score": 90,
        "trend_score": 96,
        "slope_score": 94,
        "final_score": 95,
        "prediction_bonus": 5,
    },
    {
        "ticker": "222222",
        "name": "UAT Synthetic ETF Beta",
        "rank": 2,
        "score": 82,
        "enhanced_score": 82,
        "grade": "B",
        "prediction": "MAINTAIN",
        "stability": "MEDIUM",
        "return_score": 78,
        "trend_score": 84,
        "slope_score": 80,
        "final_score": 82,
        "prediction_bonus": 2,
    },
)


def register_synthetic_ranking(app):
    """Register the synthetic ranking endpoint only."""
    if app is None:
        raise ValueError("Flask app required")

    @app.route("/api/ranking", methods=["GET"])
    def synthetic_ranking_api():
        rows = [dict(item) for item in _SYNTHETIC_ROWS]

        return jsonify({
            "success": True,
            "count": len(rows),
            "data": rows,
            "metadata": {
                "market_data_date": "2026-11-13",
                "ranking_date": "2026-11-13",
            },
        })


    @app.get("/api/historical-replay")
    def synthetic_historical_replay_api():
        from datetime import date
        from flask import request

        analysis_date = request.args.get("date", "")
        period = request.args.get("period", "3m")

        try:
            date.fromisoformat(analysis_date)
        except (ValueError, TypeError):
            return {"success": False, "message": "INVALID_DATE"}, 400

        lookbacks = {"1m": 20, "2m": 40, "3m": 60}
        if period not in lookbacks:
            return {"success": False, "message": "INVALID_PERIOD"}, 400

        rows = []
        for index, item in enumerate(_SYNTHETIC_ROWS):
            rows.append({
                "ticker": item["ticker"],
                "name": item["name"],
                "price": 10000 + index * 2000,
                "final_score": item["final_score"],
                "reality_test": {
                    "close_status": "UNAVAILABLE",
                    "high_status": "UNAVAILABLE",
                    "close_unavailable_reason": "SYNTHETIC_ONLY",
                    "high_unavailable_reason": "SYNTHETIC_ONLY",
                    "observed_days": 0,
                    "window_days": 0,
                    "close_first_hit_day": None,
                    "high_first_hit_day": None,
                },
            })

        return {
            "success": True,
            "analysis_date": analysis_date,
            "period": period,
            "lookback_trading_days": lookbacks[period],
            "market_regime": {
                "regime": "NEUTRAL",
                "confidence": 0,
            },
            "market_strategy": {
                "portfolio_mode": "balanced",
                "cash_target": 0,
            },
            "portfolio": [
                {
                    "ticker": item["ticker"],
                    "weight": 50,
                    "score": item["final_score"],
                }
                for item in _SYNTHETIC_ROWS
            ],
            "current_score_top": rows,
        }


    @app.get("/api/ver11-analysis")
    def synthetic_ver11_analysis_api():
        from datetime import date
        from flask import request

        analysis_date = request.args.get("date", "")
        period = request.args.get("period", "3m")
        sort_by = request.args.get("sort", "final_score")
        limit_text = request.args.get("limit", "10")

        try:
            date.fromisoformat(analysis_date)
        except (ValueError, TypeError):
            return {"success": False, "message": "INVALID_DATE"}, 400

        lookbacks = {"1m": 20, "2m": 40, "3m": 60}
        allowed_sorts = {
            "final_score", "return", "trend_score", "slope_score"
        }

        if period not in lookbacks:
            return {"success": False, "message": "INVALID_PERIOD"}, 400

        if sort_by not in allowed_sorts:
            return {"success": False, "message": "INVALID_SORT"}, 400

        if limit_text not in {"10", "20", "30"}:
            return {"success": False, "message": "INVALID_LIMIT"}, 400

        rows = [
            {
                **dict(item),
                "return": 4.5 if index == 0 else 2.1,
                "uptrend_ratio": 80 if index == 0 else 65,
            }
            for index, item in enumerate(_SYNTHETIC_ROWS)
        ]

        rows.sort(
            key=lambda item: item[sort_by],
            reverse=True,
        )
        rows = rows[:int(limit_text)]

        allocations = [
            {
                "ticker": item["ticker"],
                "weight": 50,
                "return_score": item["return_score"],
                "trend_score": item["trend_score"],
                "slope_score": item["slope_score"],
                "optimization_score": item["final_score"],
            }
            for item in _SYNTHETIC_ROWS
        ]

        return {
            "success": True,
            "analysis_date": analysis_date,
            "period": period,
            "lookback_trading_days": lookbacks[period],
            "current_score_top": rows,
            "market_regime": {
                "regime": "NEUTRAL",
                "confidence": 0,
            },
            "market_strategy": {
                "portfolio_mode": "balanced",
                "cash_target": 0,
            },
            "portfolio": [
                {
                    "ticker": item["ticker"],
                    "weight": 50,
                    "score": item["final_score"],
                }
                for item in _SYNTHETIC_ROWS
            ],
            "point_in_time_explanation": {
                "analysis_date": analysis_date,
                "period": period,
                "market_regime": {
                    "regime": "NEUTRAL",
                    "confidence": 0,
                    "avg_score": 0,
                    "market_strength": "SYNTHETIC_ONLY",
                },
                "market_strategy": {
                    "portfolio_mode": "balanced",
                    "cash_target": 0,
                    "recommendation": "SYNTHETIC_HOLD",
                    "rebalance_action": "NO_TRADES",
                },
                "portfolio": {
                    "cash_weight": 0,
                    "allocations": allocations,
                },
            },
        }

    return {
        ("/api/ranking", "GET"): "synthetic_ranking_api",
        ("/api/historical-replay", "GET"):
            "synthetic_historical_replay_api",
        ("/api/ver11-analysis", "GET"):
            "synthetic_ver11_analysis_api",
    }
