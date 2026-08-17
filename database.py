import sqlite3
from config import DATABASE_PATH


def get_connection():
    return sqlite3.connect(
        DATABASE_PATH,
        timeout=30
        )


def init_database():
    conn = get_connection()
    cursor = conn.cursor()

    # ETF 가격
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS etf_prices (
        ticker TEXT NOT NULL,
        date TEXT NOT NULL,
        close_price REAL NOT NULL,
        PRIMARY KEY (ticker, date)
    )
    """)

    # ETF 기본정보
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS etf_info (
        ticker TEXT PRIMARY KEY,
        name TEXT,
        market TEXT
    )
    """)

    # ETF 점수
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS etf_scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker TEXT NOT NULL,
        return_score REAL,
        trend_score REAL,
        slope_score REAL,
        final_score REAL,
        created_at TEXT
    )
    """)

    # ETF Score History
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS etf_score_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker TEXT NOT NULL,
        return_score REAL,
        trend_score REAL,
        slope_score REAL,
        final_score REAL,
        analysis_date TEXT
    )
    """)

    # ETF Ranking History
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS etf_ranking_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker TEXT NOT NULL,
        rank INTEGER,
        final_score REAL,
        ranking_date TEXT
    )
    """)


     # Portfolio History
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS portfolio_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mode TEXT NOT NULL,
        ticker TEXT NOT NULL,
        weight REAL,
        score REAL,
        reason TEXT,
        created_at TEXT
    )
    """)


    # AI Decision History
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ai_decision_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        decision TEXT,
        action TEXT,
        decision_score REAL,
        grade TEXT,
        market_view TEXT,
        recommended_mode TEXT,
        top_etf TEXT,
        reason TEXT,
        summary TEXT,
        created_at TEXT
    )
    """)


    # AI Decision Outcome History
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ai_decision_outcome_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        decision TEXT,
        action TEXT,
        strategy TEXT,
        confidence_score REAL,
        intelligence_score REAL,
        validation_score REAL,
        governance_score REAL,
        execution_score REAL,
        lifecycle_score REAL,
        operational_score REAL,
        orchestration_score REAL,
        integrated_score REAL,
        market_view TEXT,
        risk_level TEXT,
        outcome_status TEXT,
        snapshot_status TEXT,
        snapshot_purpose TEXT,
        outcome_score REAL,
        outcome_grade TEXT,
        decision_effectiveness TEXT,
        strategy_effectiveness TEXT,
        market_response TEXT,
        portfolio_response TEXT,
        learning_status TEXT,
        feedback_state TEXT,
        adaptive_learning_required INTEGER,
        reassessment_required INTEGER,
        reassessment_status TEXT,
        created_at TEXT,
        portfolio_return REAL,
        portfolio_evaluation_date TEXT,
        execution_status TEXT,
        execution_authorization TEXT,
        certification_status TEXT,
        monitoring_status TEXT,
        feedback_status TEXT
    )
    """)

    # AI Decision Outcome History Context Migration
    # Phase 6
    # Step6-10-F-12-12

    cursor.execute("PRAGMA table_info(ai_decision_outcome_history)")

    outcome_history_columns = {
        row[1]
        for row in cursor.fetchall()
    }

    outcome_history_context_columns = {
        "execution_status": "TEXT",
        "execution_authorization": "TEXT",
        "certification_status": "TEXT",
        "monitoring_status": "TEXT",
        "feedback_status": "TEXT"
    }

    for column_name, column_type in outcome_history_context_columns.items():
        if column_name not in outcome_history_columns:
            cursor.execute(
                f"""
                ALTER TABLE ai_decision_outcome_history
                ADD COLUMN {column_name} {column_type}
                """
            )

    # AI Decision Portfolio Snapshot
    # Phase 6
    # Step6-9-A
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ai_decision_portfolio_snapshot (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        history_id INTEGER NOT NULL,
        ticker TEXT NOT NULL,
        weight REAL,
        reference_price REAL,
        created_at TEXT,
        reference_price_date TEXT
    )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_database()
    print("Database initialized")