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

from core.portfolio_conversational import (
    PortfolioConversationalAnalyst
)

from core.portfolio_decision_intelligence import (
    PortfolioDecisionIntelligence
)
from core.portfolio_intelligence_score import (
    PortfolioIntelligenceScore
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
    get_ai_portfolio_optimization
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

    trend = get_ai_decision_trend()

    return jsonify(
        {
            "success": True,
            "trend": trend
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


@app.route("/api/ai-decision/adaptive-strategy")
def ai_adaptive_strategy_api():

    strategy = (
        get_ai_adaptive_strategy()
    )


    return jsonify(
        {
            "success": True,
            "strategy": strategy
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

    adaptive_strategy = (
        get_ai_adaptive_strategy()
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
            rebalance,
            optimization
        )
    )



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


    return jsonify(
        {
            "success": True,
            "intelligence": intelligence,
            "intelligence_score": intelligence_score
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
