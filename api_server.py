from flask import Flask, jsonify

from ranking_analyzer import (
    get_dashboard_api_data
)


app = Flask(__name__)



@app.route("/api/ranking")
def ranking_api():

    data = get_dashboard_api_data()


    return jsonify(
        data
    )



@app.route("/")
def home():

    return {
        "message": "GPT Quant Platform API",
        "status": "running"
    }



if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )