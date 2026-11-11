"""KIWOOM Ver1.1 offline routes for the isolated UAT Flask app.

Reuses existing price preparation, scoring and replay modules.
Does not import api_server or access operating databases, credentials,
HTTP providers, or broker services.
"""

from decimal import Decimal, InvalidOperation

from flask import jsonify, request

from kiwoom_ver11_analysis import score_kiwoom_ver11_close_prices
from kiwoom_ver11_replay import replay_kiwoom_ver11_prices


def _parse_price_rows(raw_rows):
    """Preserve the existing HTTP contract for explicit decimal-string rows."""
    if type(raw_rows) is not list or len(raw_rows) > 10000:
        raise ValueError("Invalid price collection")

    dated_closes = []
    for row in raw_rows:
        if type(row) is not list or len(row) != 2:
            raise ValueError("Invalid price row")

        observation_date, raw_close = row

        if type(raw_close) is not str:
            raise ValueError("Close must be a decimal string")

        try:
            close = Decimal(raw_close)
        except InvalidOperation as exc:
            raise ValueError("Invalid close price") from exc

        dated_closes.append((observation_date, close))

    return dated_closes


def register_kiwoom_uat_routes(app):
    """Register only the two caller-supplied offline KIWOOM endpoints."""
    if getattr(app, "_kiwoom_uat_routes_registered", False):
        raise ValueError("KIWOOM UAT routes already registered")

    @app.route("/api/kiwoom-ver11-analysis", methods=["POST"])
    def kiwoom_ver11_analysis_api():
        body = request.get_json(silent=True)

        if type(body) is not dict:
            return jsonify({
                "success": False,
                "message": "Invalid JSON body",
            }), 400

        try:
            if body.get("source") != "KIWOOM":
                raise ValueError("Explicit KIWOOM source required")

            has_prices = "prices" in body
            has_response = "response" in body

            if has_prices == has_response:
                raise ValueError("Exactly one KIWOOM price input required")

            if has_response:
                from price_provider_validation.kiwoom_ver11_price_input import (
                    prepare_kiwoom_ver11_close_prices,
                )

                dated_closes = prepare_kiwoom_ver11_close_prices(
                    body.get("api_id"),
                    body.get("ticker"),
                    body["response"],
                    requested_base_date=body.get("date"),
                )
            else:
                dated_closes = _parse_price_rows(body["prices"])

            result = score_kiwoom_ver11_close_prices(
                body.get("ticker"),
                dated_closes,
                analysis_date=body.get("date"),
                period=body.get("period", "3m"),
            )

            return jsonify({
                "success": True,
                "input_origin": "CALLER_SUPPLIED_UNVERIFIED",
                "persistence": False,
                "result": result,
            })

        except ValueError as exc:
            return jsonify({
                "success": False,
                "message": str(exc),
            }), 400

    @app.route("/api/kiwoom-ver11-replay", methods=["POST"])
    def kiwoom_ver11_replay_api():
        body = request.get_json(silent=True)

        if type(body) is not dict:
            return jsonify({
                "success": False,
                "message": "Invalid JSON body",
            }), 400

        try:
            if body.get("source") != "KIWOOM":
                raise ValueError("Explicit KIWOOM source required")

            raw_mapping = body.get("ticker_prices")

            if type(raw_mapping) is not dict or len(raw_mapping) > 5000:
                raise ValueError("Invalid ticker price mapping")

            ticker_prices = {
                ticker: _parse_price_rows(rows)
                for ticker, rows in raw_mapping.items()
            }

            result = replay_kiwoom_ver11_prices(
                ticker_prices,
                analysis_date=body.get("date"),
                period=body.get("period", "3m"),
                limit=body.get("limit", 10),
            )

            return jsonify(result)

        except ValueError as exc:
            return jsonify({
                "success": False,
                "message": str(exc),
            }), 400

    app._kiwoom_uat_routes_registered = True
    return app
