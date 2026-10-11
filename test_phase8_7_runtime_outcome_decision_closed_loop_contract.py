"""Synthetic isolated API contract; no source database copy or import-time execution."""
from contextlib import ExitStack, closing
from price_test_support import (isolated_price_db, isolated_evaluation_api,
                                synthetic_ranking_db, synthetic_ready_api)


def test_runtime_outcome_closed_loop(synthetic_ready_api):
    client = synthetic_ready_api.client
    with ExitStack() as stack:

        conn = stack.enter_context(closing(synthetic_ready_api.db.connect()))
        cursor = conn.cursor()
        entry_price, evaluation_price = 100.0, 88.0
        expected_return = round((evaluation_price - entry_price) / entry_price * 100, 4)
        assert expected_return < 0
        cursor.executemany("INSERT INTO etf_prices VALUES ('111111', ?, ?)",
                           [("2026-07-27", entry_price), ("2026-07-28", evaluation_price)])

        created_at = "2026-07-27T15:30:00+09:00"

        cursor.execute(
            """
            INSERT INTO ai_decision_outcome_history
            (
                decision,
                action,
                strategy,
                confidence_score,
                intelligence_score,
                outcome_status,
                snapshot_status,
                snapshot_purpose,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "MAINTAIN",
                "PROCEED",
                "MAINTAIN",
                93.2,
                89.6,
                "PENDING",
                "COLLECTED",
                "FUTURE_OUTCOME_EVALUATION",
                created_at,
            ),
        )

        history_id = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO ai_decision_portfolio_snapshot
            (
                history_id,
                ticker,
                weight,
                reference_price,
                created_at,
                reference_price_date
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                history_id,
                "111111",
                100.0,
                entry_price,
                created_at,
                "2026-07-27",
            ),
        )

        conn.commit()
        conn.close()

        evaluation_response = client.get(
            f"/api/ai-decision/portfolio-snapshot/"
            f"{history_id}/evaluate"
            f"?evaluation_date=2026-07-28"
        )

        assert evaluation_response.status_code == 200

        evaluation_payload = evaluation_response.get_json()

        evaluation = evaluation_payload["evaluation"]
        outcome_evaluation = evaluation_payload["outcome_evaluation"]

        print("EVALUATION STATUS :", evaluation["evaluation_status"])
        print("PORTFOLIO RETURN  :", evaluation["portfolio_return"])
        print("LEARNING SIGNAL   :", outcome_evaluation["learning_signal"])
        print(
            "ADAPTIVE REQUIRED :",
            outcome_evaluation["adaptive_learning_required"],
        )

        conn = stack.enter_context(closing(synthetic_ready_api.db.connect()))

        audit_before = conn.execute(
            "SELECT COUNT(*) FROM audit_event"
        ).fetchone()[0]

        adaptive_before = conn.execute(
            """
            SELECT COUNT(*)
            FROM audit_event
            WHERE event_type = 'ADAPTIVE_STRATEGY_GENERATED'
              AND outcome_history_id = ?
            """,
            (history_id,),
        ).fetchone()[0]

        conn.close()

        response = client.get(
            "/api/portfolio/decision-intelligence"
        )

        payload = (
            response.get_json()
            if response.is_json
            else None
        )

        conn = stack.enter_context(closing(synthetic_ready_api.db.connect()))

        audit_after = conn.execute(
            "SELECT COUNT(*) FROM audit_event"
        ).fetchone()[0]

        adaptive_after = conn.execute(
            """
            SELECT COUNT(*)
            FROM audit_event
            WHERE event_type = 'ADAPTIVE_STRATEGY_GENERATED'
              AND outcome_history_id = ?
            """,
            (history_id,),
        ).fetchone()[0]

        conn.close()

        # --------------------------------
        # Phase 8-7 Runtime Closed Loop Contract
        # --------------------------------

        assert evaluation["evaluation_status"] == "EVALUATED"
        assert evaluation["outcome_status"] == "EVALUATED"
        assert evaluation["portfolio_return"] == expected_return

        assert outcome_evaluation["learning_signal"] == "NEGATIVE"
        assert (
            outcome_evaluation["adaptive_learning_required"]
            is True
        )
        assert (
            outcome_evaluation["reassessment_required"]
            is True
        )

        assert response.status_code == 200
        assert isinstance(payload, dict)
        assert payload["success"] is True

        intelligence = payload["intelligence"]
        final_decision = payload["final_decision"]

        assert (
            intelligence["outcome_learning_signal"]
            == "NEGATIVE"
        )
        assert intelligence["adaptive_learning_required"] is True
        assert intelligence["strategy_mode"] == "DEFENSIVE"
        assert intelligence["adaptive_action"] == "REDUCE_RISK"
        assert intelligence["adaptive_override"] is True
        assert intelligence["final_strategy"] == "DEFENSIVE"

        assert final_decision["strategy"] == "DEFENSIVE"
        assert final_decision["adaptive_action"] == "REDUCE_RISK"

        assert audit_after == audit_before
        assert adaptive_after == adaptive_before

        print("DECISION HTTP     :", response.status_code)
        print("DECISION SUCCESS  :", (
            payload.get("success")
            if isinstance(payload, dict)
            else None
        ))

        print(
            "RUNTIME SIGNAL    :",
            intelligence.get("outcome_learning_signal"),
        )
        print(
            "STRATEGY MODE     :",
            intelligence.get("strategy_mode"),
        )
        print(
            "ADAPTIVE ACTION   :",
            intelligence.get("adaptive_action"),
        )
        print(
            "ADAPTIVE OVERRIDE :",
            intelligence.get("adaptive_override"),
        )
        print(
            "FINAL STRATEGY    :",
            intelligence.get("final_strategy"),
        )
        print(
            "FINAL DEC STRATEGY:",
            final_decision.get("strategy"),
        )
        print(
            "FINAL DEC ADAPTIVE:",
            final_decision.get("adaptive_action"),
        )

        print("AUDIT BEFORE      :", audit_before)
        print("AUDIT AFTER       :", audit_after)
        print("AUDIT DELTA       :", audit_after - audit_before)
        print("ADAPTIVE BEFORE   :", adaptive_before)
        print("ADAPTIVE AFTER    :", adaptive_after)
        print(
            "ADAPTIVE DELTA    :",
            adaptive_after - adaptive_before,
        )
