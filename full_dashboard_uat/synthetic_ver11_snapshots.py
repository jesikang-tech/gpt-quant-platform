"""Ephemeral synthetic Ver1.1 snapshot UI fixture.

Process-local memory only. No operating database or file persistence.
"""

from datetime import date, datetime, timezone

from flask import request

from full_dashboard_uat.synthetic_ranking import _SYNTHETIC_ROWS


def register_synthetic_ver11_snapshots(app):
    if app is None:
        raise ValueError("APP_REQUIRED")

    snapshots = {}

    @app.post("/api/ver11-analysis/snapshots")
    def synthetic_ver11_snapshot_save_api():
        body = request.get_json(silent=True)
        if type(body) is not dict:
            return {"success": False, "message": "INVALID_JSON"}, 400

        analysis_date = body.get("date")
        period = body.get("period")
        sort_by = body.get("sort")
        limit = body.get("limit")

        try:
            if type(analysis_date) is not str:
                raise ValueError("INVALID_DATE")
            date.fromisoformat(analysis_date)
        except ValueError:
            return {"success": False, "message": "INVALID_DATE"}, 400

        if period not in ("1m", "2m", "3m"):
            return {"success": False, "message": "INVALID_PERIOD"}, 400

        if sort_by not in (
            "final_score", "return", "trend_score", "slope_score"
        ):
            return {"success": False, "message": "INVALID_SORT"}, 400

        if type(limit) is not int or limit not in (10, 20, 30):
            return {"success": False, "message": "INVALID_LIMIT"}, 400

        snapshot_id = len(snapshots) + 1
        snapshot = {
            "id": snapshot_id,
            "analysis_date": analysis_date,
            "period": period,
            "sort_by": sort_by,
            "display_limit": limit,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "snapshot_payload": {
                "market_regime": {"regime": "NEUTRAL"},
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
            },
        }

        snapshots[snapshot_id] = snapshot

        return {
            "success": True,
            "snapshot": snapshot,
            "storage_scope": "SYNTHETIC_PROCESS_MEMORY_ONLY",
        }

    @app.get("/api/ver11-analysis/snapshots")
    def synthetic_ver11_snapshot_history_api():
        limit_text = request.args.get("limit", "50")

        if limit_text not in ("10", "20", "30", "50"):
            return {"success": False, "message": "INVALID_LIMIT"}, 400

        records = list(reversed(list(snapshots.values())))
        return {
            "success": True,
            "snapshots": records[:int(limit_text)],
            "storage_scope": "SYNTHETIC_PROCESS_MEMORY_ONLY",
        }

    @app.get("/api/ver11-analysis/snapshots/<snapshot_id>")
    def synthetic_ver11_snapshot_detail_api(snapshot_id):
        if not snapshot_id.isdecimal():
            return {"success": False, "message": "INVALID_ID"}, 400

        snapshot = snapshots.get(int(snapshot_id))
        if snapshot is None:
            return {"success": False, "message": "NOT_FOUND"}, 404

        return {
            "success": True,
            "snapshot": snapshot,
            "storage_scope": "SYNTHETIC_PROCESS_MEMORY_ONLY",
        }

    return {
        ("/api/ver11-analysis/snapshots", "POST"):
            "synthetic_ver11_snapshot_save_api",
        ("/api/ver11-analysis/snapshots", "GET"):
            "synthetic_ver11_snapshot_history_api",
    }
