from flask import Flask, render_template
from ai_predictor import predict_match
import requests
from datetime import datetime

app = Flask(__name__)

API_KEY = "82d298b37c1a4c078c08a99b8882e429"

headers = {
    "X-Auth-Token": API_KEY
}


def get_matches(day_offset=0):

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

    if len(dates) == 0:
        return []

    if day_offset >= len(dates):
        return []

    target_day = dates[day_offset]

    fixtures = []

    match_id = 1

    for match in data["matches"]:

        match_date = datetime.fromisoformat(
            match["utcDate"].replace("Z", "+00:00")
        ).date()

        if match_date == target_day:

            fixtures.append({
                "id": match_id,
                "home": match["homeTeam"]["name"],
                "away": match["awayTeam"]["name"]
            })

            match_id += 1

    return fixtures

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
    "away": match["awayTeam"]["name"],
    "date": str(match_date),
    "time": datetime.fromisoformat(
        match["utcDate"].replace("Z", "+00:00")
    ).strftime("%H:%M UTC")
})

            match_id += 1

    return fixtures


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/today")
def today():

    matches = get_matches(0)

    return render_template(
        "today.html",
        matches=matches
    )


@app.route("/predict/<int:match_id>")
def predict(match_id):

    matches = get_today_matches()

    selected = matches[match_id - 1]

    prediction = predict_match(
    selected["home"],
    selected["away"]
)

    return render_template(
        "predict.html",
        match=selected,
        prediction=prediction
    )


@app.route("/tomorrow")
def tomorrow():

    matches = get_matches(1)

    return render_template(
        "today.html",
        matches=matches
    )


@app.route("/all")
def all_matches():

    matches = []

    matches.extend(get_matches(0))
    matches.extend(get_matches(1))
    matches.extend(get_matches(2))

    return render_template(
        "today.html",
        matches=matches
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
