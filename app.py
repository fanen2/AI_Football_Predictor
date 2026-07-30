from flask import Flask, render_template
from ai_predictor import predict_match
import requests
from datetime import datetime

app = Flask(__name__)

API_KEY = "82d298b37c1a4c078c08a99b8882e429"

headers = {
    "X-Auth-Token": API_KEY
}


def get_today_matches():

    url = "https://api.football-data.org/v4/competitions/PL/matches"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return []

    data = response.json()

    dates = sorted(
        list(
            set(
                datetime.fromisoformat(
                    m["utcDate"].replace("Z", "+00:00")
                ).date()
                for m in data["matches"]
            )
        )
    )

    today = dates[0]

    fixtures = []

    match_id = 1

    for match in data["matches"]:

        match_date = datetime.fromisoformat(
            match["utcDate"].replace("Z", "+00:00")
        ).date()

        if match_date == today:

            fixtures.append({
                "id": match_id,
                "home": match["homeTeam"]["name"],
                "away": match["awayTeam"]["name"]
            })

            match_id += 1

    return fixtures


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/today")
def today():

    matches = get_today_matches()

    return render_template(
        "today.html",
        matches=matches
    )


@app.route("/predict/<int:match_id>")
def predict(match_id):

    matches = get_today_matches()

    selected = matches[match_id - 1]

    prediction = {
        "result": "Loading AI...",
        "confidence": "",

        "goal_market": "",
        "goal_confidence": "",

        "gg": "",
        "gg_confidence": "",

        "score": "",

        "bestbet": ""
    }

    return render_template(
        "predict.html",
        match=selected,
        prediction=prediction
    )


@app.route("/tomorrow")
def tomorrow():
    return "<h1>Tomorrow Matches Coming Soon...</h1>"


@app.route("/all")
def all_matches():
    return "<h1>Upcoming Matches Coming Soon...</h1>"


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
