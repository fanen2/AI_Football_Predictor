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
        "result": "Home Win",
        "confidence": "84%",
        "over25": "YES",
        "gg": "YES",
        "score": "2 - 1",
        "bestbet": "Home Win"
    }

    return render_template(
        "predict.html",
        match=selected,
        prediction=prediction
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
