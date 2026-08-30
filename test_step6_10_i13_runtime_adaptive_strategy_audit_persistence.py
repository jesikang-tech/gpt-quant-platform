import os
import sqlite3
import tempfile
from pathlib import Path

import config
import database
import repository

from core.ai_decision_adaptive_strategy import (
    AIDecisionAdaptiveStrategy
)


def run_test():
    fd, db_path = tempfile.mkstemp(
        prefix="step6_10_i13_",
        suffix=".db"
    )
    os.close(fd)

    original_config_path = config.DATABASE_PATH
    original_database_path = database.DATABASE_PATH

    try:
        test_db_path = Path(db_path)

        config.DATABASE_PATH = test_db_path
        database.DATABASE_PATH = test_db_path

        database.init_database()

        history_id = 201

        trend = {
            "direction": "UP",
            "stability": "HIGH",
            "momentum": "POSITIVE",
            "grade_stability": "STABLE",
            "consistency": "HIGH",
            "latest_score": 85
        }

        outcome_intelligence = {
            "outcome_status": "EVALUATED",
            "outcome_score": 80.0,
            "outcome_grade": "B",
            "outcome_learning_status":
                "LEARNING_AVAILABLE",
            "feedback_state":
                "LEARNING_AVAILABLE",
            "adaptive_learning_required":
                False,
            "reassessment_required":
                False,
            "reassessment_status":
                "NOT_REQUIRED",
            "outcome_learning_signal":
                "POSITIVE",
            "outcome_learning_signal_strength":
                0.8,
            "source_history_id":
                history_id
        }

        strategy_engine = (
            AIDecisionAdaptiveStrategy()
        )

        strategy = strategy_engine.analyze(
            trend,
            outcome_intelligence
        )

        assert strategy["strategy"] == "GROWTH"
        assert strategy["action"] == "INCREASE_RISK"
        assert (
            strategy["outcome_learning_signal"]
            == "POSITIVE"
        )
        assert (
            strategy[
                "outcome_learning_signal_strength"
            ]
            == 0.8
        )

        event_time = (
            "2026-08-30T15:00:00+09:00"
        )

        repository.save_ai_decision_audit_event(
            event_type="ADAPTIVE_STRATEGY_GENERATED",
            event_time=event_time,
            source="adaptive_strategy",
            status="GENERATED",
            outcome_history_id=history_id,
            correlation_key=(
                f"outcome:{history_id}"
            ),
            details={
                "strategy":
                    strategy["strategy"],
                "action":
                    strategy["action"],
                "outcome_learning_signal":
                    strategy[
                        "outcome_learning_signal"
                    ],
                "outcome_learning_signal_strength":
                    strategy[
                        "outcome_learning_signal_strength"
                    ],
                "adaptive_learning_required":
                    strategy[
                        "adaptive_learning_required"
                    ],
            }
        )

        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                event_type,
                status,
                source,
                outcome_history_id,
                correlation_key,
                details
            FROM audit_event
            WHERE event_type = ?
            ORDER BY id ASC
            """,
            (
                "ADAPTIVE_STRATEGY_GENERATED",
            )
        )

        events = cursor.fetchall()

        assert len(events) == 1

        event = events[0]

        assert (
            event[0]
            == "ADAPTIVE_STRATEGY_GENERATED"
        )
        assert event[1] == "GENERATED"
        assert event[2] == "adaptive_strategy"
        assert event[3] == history_id
        assert (
            event[4]
            == f"outcome:{history_id}"
        )

        assert '"strategy": "GROWTH"' in event[5]
        assert (
            '"action": "INCREASE_RISK"'
            in event[5]
        )
        assert (
            '"outcome_learning_signal": "POSITIVE"'
            in event[5]
        )

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM audit_event
            WHERE correlation_key = ?
            """,
            (
                f"outcome:{history_id}",
            )
        )

        correlation_count = (
            cursor.fetchone()[0]
        )

        assert correlation_count == 1

        print(
            "CASE 1 REAL ADAPTIVE STRATEGY: PASS | "
            f"strategy={strategy['strategy']} | "
            f"action={strategy['action']}"
        )

        print(
            "CASE 2 AUDIT PERSISTED: PASS | "
            f"events={len(events)}"
        )

        print(
            "CASE 3 CORRELATION: PASS | "
            f"correlation={event[4]}"
        )

        print(
            "CASE 4 LEARNING PAYLOAD: PASS"
        )

        print(
            "CASE 5 SINGLE CORRELATED EVENT: PASS | "
            f"events={correlation_count}"
        )

        print("")
        print("OVERALL RESULT: PASS")

        conn.close()

    finally:
        config.DATABASE_PATH = (
            original_config_path
        )
        database.DATABASE_PATH = (
            original_database_path
        )

        try:
            os.remove(db_path)
        except FileNotFoundError:
            pass


print("=" * 60)
print(
    "Step6-10-I-13 Runtime Adaptive Strategy "
    "Audit Persistence"
)
print("=" * 60)

run_test()
