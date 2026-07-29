from flask import Flask, render_template

app = Flask(__name__)

matches = [
    {
        "id": 1,
        "home": "Arsenal",
        "away": "Chelsea"
    },
    {
        "id": 2,
        "home": "Liverpool",
        "away": "Tottenham"
    },
    {
        "id": 3,
        "home": "Manchester City",
        "away": "Aston Villa"
    }
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/today")
def today():
    return render_template("today.html", matches=matches)

@app.route("/predict/<int:match_id>")
def predict(match_id):

    selected = matches[match_id - 1]

    prediction = {
        "result": "🏠 Home Win",
        "confidence": "84%",

        "goal_market": "✅ Under 2.5 Goals",
        "goal_confidence": "90%",

        "gg": "YES",
        "gg_confidence": "82%",

        "score": "2 - 0",

        "bestbet": "⭐ Under 2.5 Goals"
    }

    return render_template(
        "predict.html",
        match=selected,
        prediction=prediction
    )

@app.route("/tomorrow")
def tomorrow():
    return "<h1>Tomorrow's Matches Coming Soon...</h1>"

@app.route("/all")
def all_matches():
    return "<h1>All Upcoming Matches Coming Soon...</h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
