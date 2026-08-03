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
    optimize_portfolio_weight
)

from repository import (
    save_portfolio_history,
    get_portfolio_history
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


        for item in portfolio:

            save_portfolio_history(
                mode,
                item["ticker"],
                item.get("weight", 0),
                item.get("score", 0),
                item.get("reason", ""),
                created_at
            )


    insight = generate_portfolio_insight(
        portfolio
    )


    return jsonify(
        {
            "success": True,
            "strategy": mode.capitalize(),
            "portfolio": portfolio,
            "insight": insight
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
                "created_at": item[5]
            }
        )

    return jsonify(
        {
            "success": True,
            "history": data
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