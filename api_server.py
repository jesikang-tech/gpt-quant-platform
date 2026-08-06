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
from core.ai_decision_engine import generate_ai_decision

from repository import (
    save_portfolio_history,
    get_portfolio_history,
    get_portfolio_analytics
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


    return jsonify(

        {
            "success": True,
            "decision": decision
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


@app.route("/api/portfolio/analytics")
def portfolio_analytics_api():

    analytics = get_portfolio_analytics()

    return jsonify(
        {
            "success": True,
            "analytics": analytics
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