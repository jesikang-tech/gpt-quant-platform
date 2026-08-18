from datetime import datetime

from flask import (
    Flask,
    jsonify,
    render_template,
    request
)

from ranking_analyzer import (
    get_dashboard_api_data,
    get_ranking_history,
    get_etf_detail,
    get_dashboard_intelligence_summary,
    generate_ai_recommendation
)

from core.portfolio_advisor import (
    generate_portfolio,
    generate_portfolio_insight,
    analyze_portfolio_health,
    analyze_market_condition,
    optimize_portfolio_weight
)

from core.market_regime import analyze_market_regime

from core.market_strategy import generate_market_strategy

from core.portfolio_explainability import (
    PortfolioExplainabilityEngine
)

from core.portfolio_conversational import (
    PortfolioConversationalAnalyst
)

from core.ai_decision_engine import (
    generate_ai_decision,
    calculate_decision_score,
    get_decision_grade,
    generate_decision_intelligence
)

from core.ai_decision_explainability import (
    AIDecisionExplainability
)

from core.ai_decision_trend import (
    AIDecisionTrend
)

from core.ai_decision_adaptive_strategy import (
    AIDecisionAdaptiveStrategy
)

from core.portfolio_conversational import (
    PortfolioConversationalAnalyst
)

from core.portfolio_decision_intelligence import (
    PortfolioDecisionIntelligence
)
from core.portfolio_intelligence_score import (
    PortfolioIntelligenceScore
)

from core.decision_confidence_intelligence import (
    DecisionConfidenceIntelligence
)

from core.decision_confidence_explainability import (
    DecisionConfidenceExplainability
)

from core.decision_confidence_assessment import (
    DecisionConfidenceAssessment
)

from core.decision_confidence_recommendation import (
    DecisionConfidenceRecommendation
)

from core.ai_decision_validation import (
    AIDecisionValidation
)

from core.ai_decision_validation_explainability import (
    AIDecisionValidationExplainability
)

from core.ai_decision_validation_action import (
    AIDecisionValidationAction
)

from core.ai_final_decision_integration import (
    AIFinalDecisionIntegration
)

from core.ai_final_decision_governance import (
    AIFinalDecisionGovernance
)

from core.ai_final_decision_execution_control import (
    AIFinalDecisionExecutionControl
)

from core.ai_final_decision_execution_assurance import (
    AIFinalDecisionExecutionAssurance
)

from core.ai_final_decision_execution_monitoring import (
    AIFinalDecisionExecutionMonitoring
)

from core.ai_final_decision_execution_feedback import (
    AIFinalDecisionExecutionFeedback
)

from core.ai_final_decision_reassessment import (
    AIFinalDecisionReassessment
)

from core.ai_final_decision_lifecycle_intelligence import (
    AIFinalDecisionLifecycleIntelligence
)

from core.ai_final_decision_lifecycle_governance_control import (
    AIFinalDecisionLifecycleGovernanceControl
)

from core.ai_final_decision_operational_intelligence import (
    AIFinalDecisionOperationalIntelligence
)

from core.ai_final_decision_integrated_intelligence import (
    AIFinalDecisionIntegratedIntelligence
)

from core.ai_final_decision_orchestration import (
    AIFinalDecisionOrchestration
)

from core.ai_final_execution_decision import (
    AIFinalExecutionDecision
)

from core.ai_final_decision_certification import (
    AIFinalDecisionCertification
)

from core.ai_final_decision_master_control import (
    AIFinalDecisionMasterControl
)

from core.ai_decision_outcome_intelligence import (
    AIDecisionOutcomeIntelligence
)

from core.ai_decision_outcome_collector import (
    AIDecisionOutcomeDataCollector
)

from core.ai_decision_outcome_evaluation import (
    AIDecisionOutcomeEvaluation
)

from repository import (
    save_portfolio_history,
    get_portfolio_history,
    get_portfolio_analytics,
    save_ai_decision_history,
    get_ai_decision_history,
    get_ai_decision_summary,
    get_ai_decision_quality,
    get_ai_decision_chart_data,
    get_ai_decision_trend,
    get_ai_decision_statistics,
    get_ai_decision_performance,
    get_ai_decision_reliability,
    get_ai_adaptive_strategy,
    get_ai_rebalance_recommendation,
    get_ai_portfolio_optimization,
    save_ai_decision_outcome_history,
    get_ai_decision_outcome_history,
    get_ai_decision_outcome_learning_summary,
    get_ai_decision_outcome_history_by_id,
    update_ai_decision_outcome_history,
    save_ai_decision_portfolio_snapshot,
    get_ai_decision_portfolio_snapshot,
    evaluate_ai_decision_portfolio_snapshot
)

app = Flask(__name__)



@app.route("/api/ranking")
def ranking_api():

    data = get_dashboard_api_data()
    return jsonify(
        data
    )



@app.route("/api/intelligence")
def intelligence_api():

    data = get_dashboard_intelligence_summary()

    return jsonify(
        data
    )



@app.route("/api/recommendation/<ticker>")
def recommendation_api(ticker):

    data = generate_ai_recommendation(
        ticker
    )

    return jsonify(
        {
            "success": True,
            "ticker": ticker,
            "recommendation": data
        }
    )


@app.route("/api/market-regime")
def market_regime_api():

    data = analyze_market_regime()

    return jsonify(
        data
    )


@app.route("/api/market-strategy")
def market_strategy_api():

    market_regime = analyze_market_regime()


    strategy = generate_market_strategy(
        market_regime
    )


    return jsonify(
        strategy
    )



@app.route("/api/ai-decision")
def ai_decision_api():

    market_regime = analyze_market_regime()


    market_strategy = generate_market_strategy(
        market_regime
    )


    ranking_data = get_dashboard_api_data()


    portfolio = optimize_portfolio_weight(
        ranking_data["data"],
        "balanced"
    )


    portfolio_health = analyze_portfolio_health(
        portfolio
    )


    top_etf = {

        "ticker":
            ranking_data["data"][0]["ticker"],

        "score":
            ranking_data["data"][0]["score"]

    }


    decision = generate_ai_decision(

        market_regime,

        market_strategy,

        portfolio_health,

        top_etf

    )


    decision["decision_score"] = calculate_decision_score(
        market_regime,
        portfolio_health,
        top_etf
    )


    decision["grade"] = get_decision_grade(
        decision["decision_score"]
    )



    intelligence = generate_decision_intelligence(
        decision,
        market_regime,
        portfolio_health,
        top_etf
    )


    return jsonify(

        {
            "success": True,
            "decision": decision,
            "intelligence": intelligence
        }

    )



@app.route("/api/ai-decision/explain")
def ai_decision_explain_api():

    market_regime = analyze_market_regime()

    market_strategy = generate_market_strategy(
        market_regime
    )

    ranking_data = get_dashboard_api_data()

    portfolio = optimize_portfolio_weight(
        ranking_data["data"],
        "balanced"
    )

    portfolio_health = analyze_portfolio_health(
        portfolio
    )

    top_etf = {
        "ticker":
            ranking_data["data"][0]["ticker"],

        "score":
            ranking_data["data"][0]["score"]
    }

    decision = generate_ai_decision(
        market_regime,
        market_strategy,
        portfolio_health,
        top_etf
    )

    decision["decision_score"] = calculate_decision_score(
        market_regime,
        portfolio_health,
        top_etf
    )

    decision["grade"] = get_decision_grade(
        decision["decision_score"]
    )

    explainability = AIDecisionExplainability()

    explanation = explainability.generate_explanation(
        decision,
        market_regime,
        portfolio_health,
        top_etf
    )

    return jsonify(
        {
            "success": True,
            "explanation": explanation
        }
    )



@app.route("/api/portfolio")
def portfolio_api():

    ranking_data = get_dashboard_api_data()

    mode = request.args.get(
        "mode",
        "balanced"
    )


    save_history = request.args.get(
        "save",
        "false"
    )


    portfolio = optimize_portfolio_weight(
        ranking_data["data"],
        mode
    )


    if save_history == "true":

        from datetime import datetime

        created_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )


        intelligence = analyze_portfolio_health(
            portfolio
        )


        market_condition = analyze_market_condition(
            ranking_data["data"]
        )


        for item in portfolio:

            save_portfolio_history(
                mode,
                item["ticker"],
                item.get("weight", 0),
                item.get("score", 0),
                item.get("reason", ""),
                created_at,
                intelligence.get("health_score"),
                intelligence.get("confidence"),
                market_condition.get("market")
            )


    insight = generate_portfolio_insight(
        portfolio
    )

    intelligence = analyze_portfolio_health(
        portfolio
    )


    return jsonify(
        {
            "success": True,
            "strategy": mode.capitalize(),
            "portfolio": portfolio,
            "insight": insight,
            "intelligence": intelligence
        }
    )



@app.route("/api/portfolio/explain")
def portfolio_explain_api():

    ranking_data = get_dashboard_api_data()


    mode = request.args.get(
        "mode",
        "balanced"
    )


    portfolio = optimize_portfolio_weight(
        ranking_data["data"],
        mode
    )


    market_info = analyze_market_regime()


    engine = PortfolioExplainabilityEngine()


    explanation = engine.generate_explanation(
        {
            "allocation": {
                item["ticker"]: item.get("weight", 0)
                for item in portfolio
            },

            "cash_weight":
                10
        },

        market_info
    )


    return jsonify(
        {
            "success": True,
            "strategy": mode.capitalize(),
            "explanation": explanation
        }
    )



@app.route(
    "/api/portfolio/chat",
    methods=["POST"]
)
def portfolio_chat_api():


    data = request.json


    question = data.get(
        "question",
        ""
    )


    ranking_data = get_dashboard_api_data()


    portfolio = optimize_portfolio_weight(
        ranking_data["data"],
        "balanced"
    )


    market_info = analyze_market_regime()


    engine = PortfolioConversationalAnalyst()


    result = engine.analyze(
        question,
        portfolio,
        market_info
    )


    return jsonify(
        {
            "success": True,
            "response": result
        }
    )




@app.route("/api/portfolio/market-condition")
def portfolio_market_condition_api():

    ranking_data = get_dashboard_api_data()


    condition = analyze_market_condition(
        ranking_data["data"]
    )


    return jsonify(
        {
            "success": True,
            "market_condition": condition
        }
    )



@app.route("/api/portfolio/history")
def portfolio_history_api():

    history = get_portfolio_history()

    data = []

    for item in history:

        data.append(
            {
                "mode": item[0],
                "ticker": item[1],
                "weight": item[2],
                "score": item[3],
                "reason": item[4],
                "created_at": item[5],
                "health_score": item[6],
                "confidence": item[7],
                "market_condition": item[8]
            }
        )

    return jsonify(
        {
            "success": True,
            "history": data
        }
    )



@app.route(
    "/api/ai-decision/history"
)
def ai_decision_history_api():

    history = get_ai_decision_history()


    data = []


    for item in history:

        data.append(
            {
                "decision": item[0],
                "action": item[1],
                "decision_score": item[2],
                "grade": item[3],
                "market_view": item[4],
                "recommended_mode": item[5],
                "top_etf": item[6],
                "reason": item[7],
                "summary": item[8],
                "created_at": item[9]
            }
        )


    return jsonify(
        {
            "success": True,
            "history": data
        }
    )



@app.route("/api/ai-decision/outcome-history")
def ai_decision_outcome_history_api():

    history = get_ai_decision_outcome_history()

    data = []

    for item in history:

        data.append(
            {
                "id": item[0],
                "decision": item[1],
                "action": item[2],
                "strategy": item[3],
                "confidence_score": item[4],
                "intelligence_score": item[5],
                "validation_score": item[6],
                "governance_score": item[7],
                "execution_score": item[8],
                "lifecycle_score": item[9],
                "operational_score": item[10],
                "orchestration_score": item[11],
                "integrated_score": item[12],
                "market_view": item[13],
                "risk_level": item[14],
                "outcome_status": item[15],
                "snapshot_status": item[16],
                "snapshot_purpose": item[17],
                "outcome_score": item[18],
                "outcome_grade": item[19],
                "decision_effectiveness": item[20],
                "strategy_effectiveness": item[21],
                "market_response": item[22],
                "portfolio_response": item[23],
                "learning_status": item[24],
                "feedback_state": item[25],
                "adaptive_learning_required": bool(item[26]),
                "reassessment_required": bool(item[27]),
                "reassessment_status": item[28],
                "created_at": item[29],
                "portfolio_return": item[30],
                "portfolio_evaluation_date": item[31],
                "execution_status": item[32],
                "execution_authorization": item[33],
                "certification_status": item[34],
                "monitoring_status": item[35],
                "feedback_status": item[36]
            }
        )

    return jsonify(
        {
            "success": True,
            "history": data
        }
    )

@app.route("/api/ai-decision/outcome-learning-summary")
def ai_decision_outcome_learning_summary_api():

    summary = (
        get_ai_decision_outcome_learning_summary()
    )

    return jsonify(
        {
            "success": True,
            "summary": summary
        }
    )


@app.route(
    "/api/ai-decision/portfolio-snapshot/<int:history_id>/evaluate"
)
def ai_decision_portfolio_snapshot_evaluate_api(
    history_id
):

    evaluation_date = request.args.get(
        "evaluation_date"
    )

    portfolio_evaluation = (
        evaluate_ai_decision_portfolio_snapshot(
            history_id=history_id,
            evaluation_date=evaluation_date
        )
    )

    # --------------------------------
    # AI Decision Outcome Re-Evaluation
    # Phase 6
    # Step6-10-E
    # Step6-10-F-5 Integration
    # --------------------------------

    outcome_evaluation = None
    outcome_intelligence = None

    if (
        portfolio_evaluation.get(
            "evaluation_status"
        ) == "EVALUATED"
        and
        portfolio_evaluation.get(
            "portfolio_return"
        ) is not None
    ):

        decision_outcome_evaluation_engine = (
            AIDecisionOutcomeEvaluation()
        )

        history_row = get_ai_decision_outcome_history_by_id(
            history_id
        )

        decision_snapshot = {
            "snapshot_status": "EVALUATED",
            "snapshot_purpose":
                "FUTURE_OUTCOME_EVALUATION"
        }

        if history_row is not None:
            decision_snapshot.update(
                {
                    "decision": history_row[1],
                    "action": history_row[2],
                    "strategy": history_row[3]
                }
            )

        outcome_evaluation = (
            decision_outcome_evaluation_engine.evaluate(
                outcome_snapshot=decision_snapshot,
                actual_outcome={
                    "portfolio_return":
                        portfolio_evaluation.get(
                            "portfolio_return"
                        ),
                    "market_response":
                        "EVALUATED",
                    "portfolio_response":
                        "EVALUATED"
                }
            )
        )

        learning_signal = outcome_evaluation.get(
            "learning_signal",
            "NONE"
        )

        learning_signal_strength = outcome_evaluation.get(
            "learning_signal_strength",
            0.0
        )

        adaptive_learning_required = (
            learning_signal == "NEGATIVE"
        )

        reassessment_required = (
            learning_signal == "NEGATIVE"
        )

        if reassessment_required:
            reassessment_status = (
                "REASSESSMENT_REQUIRED"
            )
        else:
            reassessment_status = (
                "NOT_REQUIRED"
            )

        # --------------------------------
        # AI Decision Outcome Intelligence
        # Phase 6
        # Step6-10-F-5
        # --------------------------------

        outcome_intelligence_engine = (
            AIDecisionOutcomeIntelligence()
        )

        outcome_intelligence = (
            outcome_intelligence_engine.analyze(
                final_decision={
                    "decision":
                        decision_snapshot.get(
                            "decision",
                            "UNKNOWN"
                        ),
                    "action":
                        decision_snapshot.get(
                            "action",
                            "REVIEW"
                        ),
                    "strategy":
                        decision_snapshot.get(
                            "strategy",
                            "UNKNOWN"
                        )
                },
                final_decision_execution_reassessment={
                    "reassessment_required":
                        reassessment_required,
                    "reassessment_status":
                        reassessment_status
                },
                intelligence={},
                intelligence_score={
                    "intelligence_score":
                        (
                            history_row[5]
                            if history_row is not None
                            else None
                        )
                },
                decision_confidence={
                    "confidence_score":
                        (
                            history_row[4]
                            if history_row is not None
                            else None
                        )
                },
                outcome_evaluation=outcome_evaluation
            )
        )

        # --------------------------------
        # AI Decision Outcome History Update
        # --------------------------------

        update_ai_decision_outcome_history(
            history_id=history_id,
            outcome_status=outcome_evaluation.get(
                "outcome_status",
                "EVALUATED"
            ),
            outcome_score=outcome_evaluation.get(
                "outcome_score",
                0.0
            ),
            outcome_grade=outcome_evaluation.get(
                "outcome_grade",
                "N/A"
            ),
            decision_effectiveness=outcome_evaluation.get(
                "decision_effectiveness",
                "PENDING"
            ),
            strategy_effectiveness=outcome_evaluation.get(
                "strategy_effectiveness",
                "PENDING"
            ),
            market_response=outcome_evaluation.get(
                "market_response",
                "EVALUATED"
            ),
            portfolio_response=outcome_evaluation.get(
                "portfolio_response",
                "EVALUATED"
            ),
            learning_status=outcome_intelligence.get(
                "learning_status",
                outcome_evaluation.get(
                    "learning_status",
                    "LEARNING_AVAILABLE"
                )
            ),
            feedback_state=outcome_intelligence.get(
                "feedback_state",
                "EVALUATED"
            ),
            adaptive_learning_required=int(
                adaptive_learning_required
            ),
            reassessment_required=int(
                reassessment_required
            ),
            reassessment_status=reassessment_status
        )

        outcome_evaluation[
            "learning_signal_strength"
        ] = learning_signal_strength

        outcome_evaluation[
            "adaptive_learning_required"
        ] = adaptive_learning_required

        outcome_evaluation[
            "reassessment_required"
        ] = reassessment_required

        outcome_evaluation[
            "reassessment_status"
        ] = reassessment_status

    return jsonify(
        {
            "success": True,
            "evaluation": portfolio_evaluation,
            "outcome_evaluation": outcome_evaluation,
            "outcome_intelligence": outcome_intelligence
        }
    )

@app.route(
    "/api/ai-decision/outcome-history/<int:history_id>"
)
def ai_decision_outcome_history_by_id_api(
    history_id
):

    row = get_ai_decision_outcome_history_by_id(
        history_id
    )

    if row is None:
        return jsonify(
            {
                "success": False,
                "history_id": history_id,
                "error": "AI decision outcome history not found"
            }
        ), 404

    data = {
        "id": row[0],
        "decision": row[1],
        "action": row[2],
        "strategy": row[3],
        "confidence_score": row[4],
        "intelligence_score": row[5],
        "validation_score": row[6],
        "governance_score": row[7],
        "execution_score": row[8],
        "lifecycle_score": row[9],
        "operational_score": row[10],
        "orchestration_score": row[11],
        "integrated_score": row[12],
        "market_view": row[13],
        "risk_level": row[14],
        "outcome_status": row[15],
        "snapshot_status": row[16],
        "snapshot_purpose": row[17],
        "outcome_score": row[18],
        "outcome_grade": row[19],
        "decision_effectiveness": row[20],
        "strategy_effectiveness": row[21],
        "market_response": row[22],
        "portfolio_response": row[23],
        "learning_status": row[24],
        "feedback_state": row[25],
        "adaptive_learning_required": bool(row[26]),
        "reassessment_required": bool(row[27]),
        "reassessment_status": row[28],
        "created_at": row[29],
        "portfolio_return": row[30],
        "portfolio_evaluation_date": row[31],
        "execution_status": row[32],
        "execution_authorization": row[33],
        "certification_status": row[34],
        "monitoring_status": row[35],
        "feedback_status": row[36]
    }

    return jsonify(
        {
            "success": True,
            "history": data
        }
    )

@app.route("/api/ai-decision/summary")
def ai_decision_summary_api():

    summary = get_ai_decision_summary()


    return jsonify(
        {
            "success": True,
            "summary": summary
        }
    )


@app.route("/api/ai-decision/quality")
def ai_decision_quality_api():

    quality = get_ai_decision_quality()

    return jsonify(
        {
            "success": True,
            "quality": quality
        }
    )


@app.route("/api/ai-decision/trend")
def ai_decision_trend_api():

    history = get_ai_decision_history(
        limit=10
    )

    trend_engine = AIDecisionTrend()

    trend = trend_engine.analyze(
        [
            {
                "decision_score": item[2],
                "grade": item[3],
                "decision": item[0],
                "created_at": item[9]
            }
            for item in history
        ]
    )

    # Backward compatibility
    trend["trend"] = {
        "UP": "Improving",
        "DOWN": "Declining",
        "STABLE": "Stable"
    }.get(
        trend.get("direction"),
        "UNKNOWN"
    )

    trend["average_change"] = (
        trend.get("score_change", 0)
    )

    return jsonify(
        {
            "success": True,
            "trend": trend
        }
    )



@app.route("/api/ai-decision/adaptive-strategy")
def ai_decision_adaptive_strategy_api():

    history = get_ai_decision_history(
        limit=10
    )

    trend_engine = AIDecisionTrend()

    trend = trend_engine.analyze(
        [
            {
                "decision_score": item[2],
                "grade": item[3],
                "decision": item[0],
                "created_at": item[9]
            }
            for item in history
        ]
    )

    # --------------------------------
    # Step6-10-F-12
    # Bridge Outcome Intelligence
    # into Adaptive Strategy API
    # --------------------------------

    outcome_intelligence = {}

    outcome_history = get_ai_decision_outcome_history(
        limit=50
    )

    for outcome_row in outcome_history:

        if outcome_row[15] != "EVALUATED":
            continue

        outcome_score = outcome_row[18]

        if outcome_score is None:
            outcome_score = 0.0

        outcome_intelligence = {
            "outcome_status": outcome_row[15],
            "outcome_score": outcome_score,
            "outcome_grade": outcome_row[19],
            "outcome_learning_status": outcome_row[24],
            "feedback_state": outcome_row[25],
            "adaptive_learning_required": bool(outcome_row[26]),
            "reassessment_required": bool(outcome_row[27]),
            "reassessment_status": outcome_row[28],
            "outcome_learning_signal": (
                "NEGATIVE"
                if bool(outcome_row[26]) and outcome_score < 50
                else "POSITIVE"
                if not bool(outcome_row[26]) and outcome_score >= 70
                else "NONE"
            ),
            "outcome_learning_signal_strength": abs(outcome_score),
            "source_history_id": outcome_row[0]
        }

        break

    strategy_engine = AIDecisionAdaptiveStrategy()

    strategy = strategy_engine.analyze(
        trend,
        outcome_intelligence
    )

    return jsonify(
        {
            "success": True,
            "strategy": strategy,
            "outcome_intelligence": outcome_intelligence
        }
    )



@app.route("/api/ai-decision/chart")
def ai_decision_chart_api():

    chart = get_ai_decision_chart_data()

    return jsonify(
        {
            "success": True,
            "chart": chart
        }
    )


@app.route("/api/ai-decision/statistics")
def ai_decision_statistics_api():

    statistics = get_ai_decision_statistics()

    return jsonify(
        {
            "success": True,
            "statistics": statistics
        }
    )


@app.route("/api/ai-decision/performance")
def ai_decision_performance_api():

    performance = (
        get_ai_decision_performance()
    )


    return jsonify(
        {
            "success": True,
            "performance": performance
        }
    )


@app.route("/api/ai-decision/reliability")
def ai_decision_reliability_api():

    reliability = (
        get_ai_decision_reliability()
    )


    return jsonify(
        {
            "success": True,
            "reliability": reliability
        }
    )




@app.route("/api/portfolio/ai-rebalance")
def ai_rebalance_api():

    recommendation = (
        get_ai_rebalance_recommendation()
    )


    return jsonify(
        {
            "success": True,
            "recommendation": recommendation
        }
    )



@app.route("/api/portfolio/ai-optimization")
def ai_portfolio_optimization_api():

    optimization = (
        get_ai_portfolio_optimization()
    )


    return jsonify(
        {
            "success": True,
            "optimization": optimization
        }
    )


@app.route("/api/portfolio/analytics")
def portfolio_analytics_api():

    analytics = get_portfolio_analytics()

    return jsonify(
        {
            "success": True,
            "analytics": analytics
        }
    )



@app.route("/api/portfolio/decision-intelligence")
def portfolio_decision_intelligence_api():

    # -----------------------------
    # AI Decision
    # -----------------------------

    market_regime = analyze_market_regime()

    market_strategy = generate_market_strategy(
        market_regime
    )

    ranking_data = get_dashboard_api_data()

    portfolio = optimize_portfolio_weight(
        ranking_data["data"],
        "balanced"
    )

    portfolio_health = analyze_portfolio_health(
        portfolio
    )

    top_etf = {
        "ticker":
            ranking_data["data"][0]["ticker"],

        "score":
            ranking_data["data"][0]["score"]
    }

    ai_decision = generate_ai_decision(
        market_regime,
        market_strategy,
        portfolio_health,
        top_etf
    )

    ai_decision["decision_score"] = (
        calculate_decision_score(
            market_regime,
            portfolio_health,
            top_etf
        )
    )

    ai_decision["grade"] = get_decision_grade(
        ai_decision["decision_score"]
    )


    # -----------------------------
    # Decision Quality
    # -----------------------------

    decision_quality = (
        get_ai_decision_quality()
    )


    # -----------------------------
    # Reliability
    # -----------------------------

    reliability = (
        get_ai_decision_reliability()
    )


    # -----------------------------
    # Adaptive Strategy
    # -----------------------------

    adaptive_history = get_ai_decision_history(
        limit=10
    )

    adaptive_trend_engine = AIDecisionTrend()

    adaptive_trend = adaptive_trend_engine.analyze(
        [
            {
                "decision_score": item[2],
                "grade": item[3],
                "decision": item[0],
                "created_at": item[9]
            }
            for item in adaptive_history
        ]
    )

    adaptive_strategy_engine = (
        AIDecisionAdaptiveStrategy()
    )

    adaptive_strategy = adaptive_strategy_engine.analyze(
        adaptive_trend
    )
# -----------------------------
    # Rebalance
    # -----------------------------

    rebalance = (
        get_ai_rebalance_recommendation()
    )


    # -----------------------------
    # Portfolio Optimization
    # -----------------------------

    optimization = (
        get_ai_portfolio_optimization()
    )


    # -----------------------------
    # Explainability
    # -----------------------------

    explainability_engine = (
        PortfolioExplainabilityEngine()
    )

    explainability = (
        explainability_engine.generate_explanation(
            portfolio,
            market_regime
        )
    )



    # -----------------------------
    # Final Decision Intelligence
    # -----------------------------

    engine = (
        PortfolioDecisionIntelligence()
    )

    intelligence = engine.generate(
        ai_decision,
        decision_quality,
        reliability,
        adaptive_strategy,
        rebalance,
        optimization,
        explainability
    )


    # -----------------------------
    # Portfolio Intelligence Score
    # -----------------------------

    intelligence_engine = (
        PortfolioIntelligenceScore()
    )

    intelligence_score = (
        intelligence_engine.calculate(
            ai_decision.get(
                "decision_score",
                0
            ),
            decision_quality,
            reliability,
            adaptive_strategy,
            intelligence.get(
                "decision_consistency_score",
                0
            ),
            rebalance,
            optimization
        )
    )


    # -----------------------------
    # Decision Confidence Intelligence
    # Step5-3-80
    # -----------------------------

    confidence_engine = (
        DecisionConfidenceIntelligence()
    )

    decision_confidence = (
        confidence_engine.calculate(
            decision_quality,
            reliability,
            adaptive_strategy,
            intelligence.get(
                "decision_consistency_score",
                0
            ),
            rebalance,
            optimization
        )
    )

    # -----------------------------
    # Decision Confidence Explainability
    # Step5-3-81
    # -----------------------------

    confidence_explainability_engine = (
        DecisionConfidenceExplainability()
    )

    decision_confidence_explainability = (
        confidence_explainability_engine.explain(
            decision_confidence
        )
    )


    # -----------------------------
    # Decision Confidence Assessment
    # Step5-3-82
    # -----------------------------

    confidence_assessment_engine = (
        DecisionConfidenceAssessment()
    )

    decision_confidence_assessment = (
        confidence_assessment_engine.assess(
            decision_confidence_explainability
        )
    )


    # -----------------------------
    # Decision Confidence Recommendation
    # Step5-3-83
    # -----------------------------

    confidence_recommendation_engine = (
        DecisionConfidenceRecommendation()
    )

    decision_confidence_recommendation = (
        confidence_recommendation_engine.recommend(
            decision_confidence_assessment,
            intelligence
        )
    )

    # -----------------------------
    # AI Decision Validation
    # Step5-3-84
    # -----------------------------

    decision_validation_engine = (
        AIDecisionValidation()
    )

    ai_decision_validation = (
        decision_validation_engine.validate(
            intelligence,
            decision_confidence,
            decision_confidence_assessment,
            decision_confidence_recommendation
        )
    )

    # -----------------------------
    # AI Decision Validation Explainability
    # Step5-3-85
    # -----------------------------

    validation_explainability_engine = (
        AIDecisionValidationExplainability()
    )

    ai_decision_validation_explainability = (
        validation_explainability_engine.explain(
            ai_decision_validation,
            decision_confidence,
            decision_confidence_assessment,
            decision_confidence_recommendation
        )
    )

    # -----------------------------
    # AI Decision Validation Action
    # Step5-3-86
    # -----------------------------

    validation_action_engine = (
    AIDecisionValidationAction()
)

    ai_decision_validation_action = (
        validation_action_engine.decide(
            ai_decision_validation,
            decision_confidence,
            decision_confidence_assessment,
            decision_confidence_recommendation
        )
    )

    # -----------------------------
    # AI Final Decision Integration
    # Step5-3-87
    # -----------------------------

    final_decision_engine = (
        AIFinalDecisionIntegration()
    )

    final_decision = (
        final_decision_engine.integrate(
            intelligence,
            intelligence_score,
            decision_confidence,
            decision_confidence_assessment,
            decision_confidence_recommendation,
            ai_decision_validation,
            ai_decision_validation_explainability,
            ai_decision_validation_action
        )
    )

    # -----------------------------
    # AI Final Decision Governance
    # Step5-3-88
    # -----------------------------

    final_decision_governance_engine = (
        AIFinalDecisionGovernance()
    )

    final_decision_governance = (
        final_decision_governance_engine.govern(
            final_decision,
            intelligence,
            intelligence_score,
            decision_confidence,
            ai_decision_validation,
            ai_decision_validation_action
        )
    )

    # -----------------------------
    # AI Final Decision Execution Control
    # Step5-3-89
    # -----------------------------

    final_decision_execution_control_engine = (
        AIFinalDecisionExecutionControl()
    )

    final_decision_execution_control = (
        final_decision_execution_control_engine.control(
            final_decision,
            final_decision_governance
        )
    )

    # -----------------------------
    # AI Final Decision Execution Assurance
    # Step5-3-90
    # -----------------------------

    final_decision_execution_assurance_engine = (
        AIFinalDecisionExecutionAssurance()
    )

    final_decision_execution_assurance = (
        final_decision_execution_assurance_engine.assure(
            final_decision,
            final_decision_governance,
            final_decision_execution_control
        )
    )

    # -----------------------------
    # AI Final Decision Execution Monitoring
    # Step5-3-91
    # -----------------------------

    final_decision_execution_monitoring_engine = (
        AIFinalDecisionExecutionMonitoring()
    )

    final_decision_execution_monitoring = (
        final_decision_execution_monitoring_engine.monitor(
            final_decision,
            final_decision_governance,
            final_decision_execution_control,
            final_decision_execution_assurance
        )
    )


    # -----------------------------
    # AI Final Decision Execution Feedback Intelligence
    # Step5-3-92
    # -----------------------------

    final_decision_execution_feedback_engine = (
        AIFinalDecisionExecutionFeedback()
    )

    final_decision_execution_feedback = (
        final_decision_execution_feedback_engine.feedback(
            final_decision,
            final_decision_governance,
            final_decision_execution_control,
            final_decision_execution_assurance,
            final_decision_execution_monitoring
        )
    )

    # -----------------------------
    # AI Final Decision Reassessment Intelligence
    # Step5-3-93
    # -----------------------------

    final_decision_execution_reassessment_engine = (
        AIFinalDecisionReassessment()
    )

    final_decision_execution_reassessment = (
        final_decision_execution_reassessment_engine.reassess(
            final_decision,
            final_decision_governance,
            final_decision_execution_control,
            final_decision_execution_assurance,
            final_decision_execution_feedback,
            final_decision_execution_monitoring
        )
    )

    # -----------------------------
    # AI Final Decision Lifecycle Intelligence
    # Step5-3-94
    # -----------------------------

    final_decision_lifecycle_engine = (
        AIFinalDecisionLifecycleIntelligence()
    )

    final_decision_lifecycle = (
        final_decision_lifecycle_engine.analyze(
            final_decision,
            final_decision_governance,
            final_decision_execution_control,
            final_decision_execution_assurance,
            final_decision_execution_monitoring,
            final_decision_execution_feedback,
            final_decision_execution_reassessment
        )
    )


    # -----------------------------
    # AI Final Decision Lifecycle Governance & Control
    # Step5-3-95
    # -----------------------------

    final_decision_lifecycle_governance_control_engine = (
        AIFinalDecisionLifecycleGovernanceControl()
    )

    final_decision_lifecycle_governance_control = (
        final_decision_lifecycle_governance_control_engine.govern(
            final_decision,
            final_decision_governance,
            final_decision_execution_control,
            final_decision_execution_assurance,
            final_decision_execution_monitoring,
            final_decision_execution_feedback,
            final_decision_execution_reassessment,
            final_decision_lifecycle,
            decision_confidence,
            ai_decision_validation
        )
    )


    # -----------------------------
    # AI Final Decision Operational Intelligence
    # Step5-3-96
    # -----------------------------

    final_decision_operational_intelligence_engine = (
        AIFinalDecisionOperationalIntelligence()
    )

    final_decision_operational_intelligence = (
        final_decision_operational_intelligence_engine.analyze(
            final_decision,
            final_decision_lifecycle_governance_control
        )
    )

    # -----------------------------
    # AI Final Decision Integrated Intelligence
    # Step5-3-97
    # -----------------------------

    final_decision_integrated_intelligence_engine = (
        AIFinalDecisionIntegratedIntelligence()
    )

    final_decision_integrated_intelligence = (
        final_decision_integrated_intelligence_engine.analyze(
            final_decision,
            ai_decision_validation,
            final_decision_governance,
            final_decision_execution_control,
            final_decision_execution_assurance,
            final_decision_execution_monitoring,
            final_decision_execution_feedback,
            final_decision_execution_reassessment,
            final_decision_lifecycle,
            final_decision_lifecycle_governance_control,
            final_decision_operational_intelligence
        )
    )


    # -----------------------------
    # AI Final Decision Orchestration
    # Step5-3-98
    # -----------------------------

    final_decision_orchestration_engine = (
        AIFinalDecisionOrchestration()
    )

    final_decision_orchestration = (
        final_decision_orchestration_engine.analyze(
            final_decision,
            final_decision_integrated_intelligence,
            final_decision_lifecycle_governance_control,
            final_decision_operational_intelligence
        )
    )


    # -----------------------------
    # AI Final Execution Decision
    # Step5-3-99
    # -----------------------------

    final_execution_decision_engine = (
        AIFinalExecutionDecision()
    )

    final_execution_decision = (
        final_execution_decision_engine.analyze(
            final_decision,
            final_decision_orchestration,
            final_decision_integrated_intelligence,
            final_decision_lifecycle_governance_control,
            final_decision_operational_intelligence
        )
    )


    # -----------------------------
    # AI Final Decision Certification
    # Step5-3-100
    # -----------------------------

    final_decision_certification_engine = (
        AIFinalDecisionCertification()
    )

    final_decision_certification = (
        final_decision_certification_engine.analyze(
            final_decision,
            ai_decision_validation,
            final_decision_governance,
            final_decision_lifecycle,
            final_decision_operational_intelligence,
            final_decision_integrated_intelligence,
            final_decision_orchestration,
            final_execution_decision
        )
    )



    # -----------------------------
    # AI Final Decision Master Control
    # Step5-3-101
    # -----------------------------

    final_decision_master_control_engine = (
        AIFinalDecisionMasterControl()
    )

    final_decision_master_control = (
        final_decision_master_control_engine.analyze(
            final_decision,
            final_decision_certification,
            final_execution_decision,
            final_decision_governance,
            final_decision_lifecycle,
            final_decision_operational_intelligence,
            final_decision_orchestration,
            final_decision_integrated_intelligence,
            ai_decision_validation
        )
    )



    # -----------------------------
    # AI Decision Outcome Data Collector
    # Phase 6
    # Step6-2
    # -----------------------------

    decision_outcome_collector_engine = (
        AIDecisionOutcomeDataCollector()
    )

    decision_outcome_snapshot = (
        decision_outcome_collector_engine.collect(
            final_decision,
            final_decision_master_control,
            final_decision_certification,
            final_execution_decision,
            final_decision_execution_feedback,
            final_decision_execution_monitoring,
            final_decision_execution_reassessment,
            final_decision_governance,
            final_decision_lifecycle,
            final_decision_operational_intelligence,
            final_decision_orchestration,
            final_decision_integrated_intelligence,
            intelligence,
            intelligence_score,
            decision_confidence
        )
    )

    # -----------------------------
    # AI Decision Outcome Evaluation
    # Phase 6
    # Step6-4
    # -----------------------------

    decision_outcome_evaluation_engine = (
        AIDecisionOutcomeEvaluation()
    )

    decision_outcome_evaluation = (
        decision_outcome_evaluation_engine.evaluate(
            outcome_snapshot=decision_outcome_snapshot,
            actual_outcome={}
        )
    )


    # -----------------------------
    # AI Decision Outcome Intelligence
    # Phase 6
    # Step6-1
    # Step6-5 Integration
    # -----------------------------

    decision_outcome_engine = (
        AIDecisionOutcomeIntelligence()
    )

    decision_outcome_intelligence = (
        decision_outcome_engine.analyze(
            final_decision,
            final_decision_master_control,
            final_decision_certification,
            final_execution_decision,
            final_decision_execution_feedback,
            final_decision_execution_monitoring,
            final_decision_execution_reassessment,
            intelligence,
            intelligence_score,
            decision_confidence,
            decision_outcome_evaluation
        )
    )



    # -----------------------------
    # AI Decision Outcome History
    # Phase 6
    # Step6-3
    # -----------------------------

    history_id = save_ai_decision_outcome_history(
        decision=decision_outcome_snapshot.get(
            "decision",
            "UNKNOWN"
        ),
        action=decision_outcome_snapshot.get(
            "action",
            "REVIEW"
        ),
        strategy=decision_outcome_snapshot.get(
            "strategy",
            "UNKNOWN"
        ),
        confidence_score=decision_outcome_snapshot.get(
            "confidence_score"
        ),
        intelligence_score=decision_outcome_snapshot.get(
            "intelligence_score"
        ),
        validation_score=decision_outcome_snapshot.get(
            "validation_score"
        ),
        governance_score=decision_outcome_snapshot.get(
            "governance_score"
        ),
        execution_score=decision_outcome_snapshot.get(
            "execution_score"
        ),
        lifecycle_score=decision_outcome_snapshot.get(
            "lifecycle_score"
        ),
        operational_score=decision_outcome_snapshot.get(
            "operational_score"
        ),
        orchestration_score=decision_outcome_snapshot.get(
            "orchestration_score"
        ),
        integrated_score=decision_outcome_snapshot.get(
            "integrated_score"
        ),
        market_view=decision_outcome_snapshot.get(
            "market_view",
            "UNKNOWN"
        ),
        risk_level=decision_outcome_snapshot.get(
            "risk_level",
            "UNKNOWN"
        ),
        outcome_status=decision_outcome_evaluation.get(
            "outcome_status",
            "PENDING"
        ),
        snapshot_status=decision_outcome_snapshot.get(
            "snapshot_status",
            "COLLECTED"
        ),
        snapshot_purpose=decision_outcome_snapshot.get(
            "snapshot_purpose",
            "FUTURE_OUTCOME_EVALUATION"
        ),
        outcome_score=decision_outcome_evaluation.get(
            "outcome_score",
            0.0
        ),
        outcome_grade=decision_outcome_evaluation.get(
            "outcome_grade",
            "N/A"
        ),
        decision_effectiveness=decision_outcome_evaluation.get(
            "decision_effectiveness",
            "PENDING"
        ),
        strategy_effectiveness=decision_outcome_evaluation.get(
            "strategy_effectiveness",
            "PENDING"
        ),
        market_response=decision_outcome_evaluation.get(
            "market_response",
            "PENDING"
        ),
        portfolio_response=decision_outcome_evaluation.get(
            "portfolio_response",
            "PENDING"
        ),
        learning_status=decision_outcome_intelligence.get(
            "learning_status",
            "WAITING_FOR_OUTCOME"
        ),
        feedback_state=decision_outcome_intelligence.get(
            "feedback_state",
            "COLLECTING"
        ),
        adaptive_learning_required=int(
            bool(
                decision_outcome_intelligence.get(
                    "adaptive_learning_required",
                    False
                )
            )
        ),
        reassessment_required=int(
            bool(
                decision_outcome_snapshot.get(
                    "reassessment_required",
                    False
                )
            )
        ),
        reassessment_status=decision_outcome_snapshot.get(
            "reassessment_status",
            "NOT_REQUIRED"
        ),
        created_at=datetime.now().astimezone().isoformat(),
        execution_status=decision_outcome_snapshot.get(
            "execution_status",
            "UNKNOWN"
        ),
        execution_authorization=decision_outcome_snapshot.get(
            "execution_authorization",
            "UNKNOWN"
        ),
        certification_status=decision_outcome_snapshot.get(
            "certification_status",
            "UNKNOWN"
        ),
        monitoring_status=decision_outcome_snapshot.get(
            "monitoring_status",
            "UNKNOWN"
        ),
        feedback_status=decision_outcome_snapshot.get(
            "feedback_status",
            "UNKNOWN"
        )
    )


    # -----------------------------
    # AI Decision Portfolio Snapshot
    # Phase 6
    # Step6-4-1-C
    # -----------------------------

    portfolio_snapshot_created_at = (
        datetime.now().astimezone().isoformat()
    )

    save_ai_decision_portfolio_snapshot(
        history_id=history_id,
        portfolio=portfolio,
        created_at=portfolio_snapshot_created_at
    )

    # AI Decision Outcome History Update
    # Phase 6
    # Step6-4
    # -----------------------------

    update_ai_decision_outcome_history(
        history_id=history_id,
        outcome_status=decision_outcome_evaluation.get(
            "outcome_status",
            "PENDING"
        ),
        outcome_score=decision_outcome_evaluation.get(
            "outcome_score",
            0.0
        ),
        outcome_grade=decision_outcome_evaluation.get(
            "outcome_grade",
            "N/A"
        ),
        decision_effectiveness=decision_outcome_evaluation.get(
            "decision_effectiveness",
            "PENDING"
        ),
        strategy_effectiveness=decision_outcome_evaluation.get(
            "strategy_effectiveness",
            "PENDING"
        ),
        market_response=decision_outcome_evaluation.get(
            "market_response",
            "PENDING"
        ),
        portfolio_response=decision_outcome_evaluation.get(
            "portfolio_response",
            "PENDING"
        ),
        learning_status=decision_outcome_intelligence.get(
            "learning_status",
            "WAITING_FOR_OUTCOME"
        ),
        feedback_state=decision_outcome_intelligence.get(
            "feedback_state",
            "COLLECTING"
        ),
        adaptive_learning_required=int(
            bool(
                decision_outcome_intelligence.get(
                    "adaptive_learning_required",
                    False
                )
            )
        ),
        reassessment_required=int(
            bool(
                decision_outcome_snapshot.get(
                    "reassessment_required",
                    False
                )
            )
        ),
        reassessment_status=decision_outcome_snapshot.get(
            "reassessment_status",
            "NOT_REQUIRED"
        )
    )


    return jsonify(

        {
            "success": True,
            "intelligence": intelligence,
            "intelligence_score": intelligence_score,
            "decision_confidence": decision_confidence,
            "decision_confidence_explainability": decision_confidence_explainability,
            "decision_confidence_assessment": decision_confidence_assessment,
            "decision_confidence_recommendation": decision_confidence_recommendation,
            "ai_decision_validation": ai_decision_validation,
            "ai_decision_validation_explainability":
                ai_decision_validation_explainability,
            "ai_decision_validation_action":
                ai_decision_validation_action,
            "final_decision":
                final_decision,
            "final_decision_governance":
                final_decision_governance,
            "final_decision_execution_control":
                final_decision_execution_control,
            "final_decision_execution_assurance":
                final_decision_execution_assurance,
            "final_decision_execution_monitoring":
                final_decision_execution_monitoring,
            "final_decision_execution_feedback":
                final_decision_execution_feedback,
            "final_decision_execution_reassessment":
                final_decision_execution_reassessment,
            "final_decision_lifecycle":
                final_decision_lifecycle,
            "final_decision_lifecycle_governance_control":
                final_decision_lifecycle_governance_control,
            "final_decision_operational_intelligence":
                final_decision_operational_intelligence,
            "final_decision_integrated_intelligence":
                final_decision_integrated_intelligence,
            "final_decision_orchestration":
                final_decision_orchestration,
            "final_execution_decision":
                final_execution_decision,
            "final_decision_certification":
                final_decision_certification,
            "ai_decision_outcome_intelligence":
                decision_outcome_intelligence,
            "ai_decision_outcome_snapshot":
                decision_outcome_snapshot,
            "ai_decision_outcome_evaluation":
                decision_outcome_evaluation,
            "final_decision_master_control":
                final_decision_master_control
        }
    )


@app.route("/api/history/<ticker>")
def history_api(ticker):


    history = get_ranking_history(
        ticker
    )


    data = []


    for item in history:

        data.append(
            {
                "date": item[3],
                "rank": item[1],
                "score": item[2]
            }
        )


    return jsonify(
        {
            "ticker": ticker,
            "history": data
        }
    )



@app.route("/api/detail/<ticker>")
def detail_api(ticker):


    data = get_etf_detail(
        ticker
    )


    return jsonify(
        data
    )



@app.route("/")
def home():

    return render_template(
        "index.html"
    )



if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
