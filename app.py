from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/today")
def today():
    matches = [
        {
            "home": "Arsenal",
            "away": "Chelsea"
        },
        {
            "home": "Liverpool",
            "away": "Tottenham"
        },
        {
            "home": "Manchester City",
            "away": "Aston Villa"
        }
    ]

    return render_template(
        "today.html",
        matches=matches
    )

@app.route("/tomorrow")
def tomorrow():
    return "<h1>Tomorrow's Matches Coming Soon...</h1>"

@app.route("/all")
def all_matches():
    return "<h1>All Upcoming Matches Coming Soon...</h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
