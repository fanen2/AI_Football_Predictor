import pandas as pd
import joblib

from sklearn.preprocessing import LabelEncoder
TEAM_MAP = {
    "Arsenal FC": "Arsenal",
    "Chelsea FC": "Chelsea",
    "Liverpool FC": "Liverpool",
    "Manchester City FC": "Man City",
    "Manchester United FC": "Man United",
    "Tottenham Hotspur FC": "Tottenham",
    "Newcastle United FC": "Newcastle",
    "Aston Villa FC": "Aston Villa",
    "Brighton & Hove Albion FC": "Brighton",
    "West Ham United FC": "West Ham",
    "Everton FC": "Everton",
    "Crystal Palace FC": "Crystal Palace",
    "Brentford FC": "Brentford",
    "Fulham FC": "Fulham",
    "Wolverhampton Wanderers FC": "Wolves",
    "AFC Bournemouth": "Bournemouth",
    "Nottingham Forest FC": "Nottingham Forest",
    "Leicester City FC": "Leicester",
    "Southampton FC": "Southampton",
    "Ipswich Town FC": "Ipswich"
}

print("=" * 50)
print("Loading AI Prediction Engine...")
print("=" * 50)

# ==========================
# LOAD DATASET
# ==========================

data = pd.read_csv(
    "/storage/emulated/0/Download/final_ai_dataset.csv"
).dropna()

print("Dataset Loaded Successfully!")

# ==========================
# LOAD AI MODELS
# ==========================

match_ai = joblib.load("match_result_ai_v6.pkl")

match_result_encoder = joblib.load("match_result_encoder_v6.pkl")

over25_ai = joblib.load("over25_ai_v1.pkl")

over35_ai = joblib.load("over35_ai_v1.pkl")

btts_ai = joblib.load("btts_ai_v1.pkl")

correct_score_ai = joblib.load("correct_score_ai_v2.pkl")

correct_score_encoder = joblib.load("correct_score_encoder_v2.pkl")

print("All AI Models Loaded Successfully!")

# ==========================
# TEAM ENCODER
# ==========================

team_encoder = LabelEncoder()

team_encoder.fit(
    pd.concat([
        data["HomeTeam"],
        data["AwayTeam"]
    ])
)

print("Team Encoder Ready!")
# ==========================================
# MAIN AI FUNCTION
# ==========================================

def predict_match(home_team, away_team):

    print("=" * 50)
    print("Starting AI Prediction...")
    print("=" * 50)

    # --------------------------
    # MAP TEAM NAMES
    # --------------------------

    home_team = TEAM_MAP.get(home_team, home_team)
    away_team = TEAM_MAP.get(away_team, away_team)

    print("Mapped Teams:")
    print(home_team, "vs", away_team)

    # --------------------------
    # LOAD TEAM HISTORY
    # --------------------------

    home_history = data[
        data["HomeTeam"] == home_team
    ]

    if home_history.empty:
        raise Exception(
            f"No history found for {home_team}"
        )

    home_record = home_history.iloc[-1]

    away_history = data[
        data["AwayTeam"] == away_team
    ]

    if away_history.empty:
        raise Exception(
            f"No history found for {away_team}"
        )

    away_record = away_history.iloc[-1]

    print("Historical Data Loaded Successfully!")

    # --------------------------
    # BUILD FEATURE VECTOR
    # --------------------------

    feature_vector = pd.DataFrame([{

        "HomeTeam": team_encoder.transform([home_team])[0],
        "AwayTeam": team_encoder.transform([away_team])[0],

        "HomeRecentPoints": home_record["HomeRecentPoints"],
        "AwayRecentPoints": away_record["AwayRecentPoints"],

        "HomeWinRate": home_record["HomeWinRate"],
        "AwayWinRate": away_record["AwayWinRate"],

        "H2HHomeWins": home_record["H2HHomeWins"],
        "H2HAwayWins": home_record["H2HAwayWins"],
        "H2HDraws": home_record["H2HDraws"],
        "H2HGoalsAvg": home_record["H2HGoalsAvg"],

        "HomeAttackStrength": home_record["HomeAttackStrength"],
        "AwayAttackStrength": away_record["AwayAttackStrength"],

        "HomeDefenseStrength": home_record["HomeDefenseStrength"],
        "AwayDefenseStrength": away_record["AwayDefenseStrength"],

        "ExpectedHomeGoals": home_record["ExpectedHomeGoals"],
        "ExpectedAwayGoals": away_record["ExpectedAwayGoals"]

    }])

    print("Feature Vector Created Successfully!")
     # ==========================
    # MATCH RESULT AI
    # ==========================

    match_prediction = match_ai.predict(feature_vector)[0]

    match_prediction = match_result_encoder.inverse_transform(
        [match_prediction]
    )[0]

    match_probability = match_ai.predict_proba(feature_vector)[0]

    match_confidence = round(
        max(match_probability) * 100,
        2
    )

    # ==========================
    # OVER 2.5 AI
    # ==========================

    over25_prediction = over25_ai.predict(feature_vector)[0]

    over25_probability = over25_ai.predict_proba(feature_vector)[0]

    over25_confidence = round(
        max(over25_probability) * 100,
        2
    )

    # ==========================
    # OVER 3.5 AI
    # ==========================

    over35_prediction = over35_ai.predict(feature_vector)[0]

    over35_probability = over35_ai.predict_proba(feature_vector)[0]

    over35_confidence = round(
        max(over35_probability) * 100,
        2
    )

    # ==========================
    # BTTS AI
    # ==========================

    btts_prediction = btts_ai.predict(feature_vector)[0]

    btts_probability = btts_ai.predict_proba(feature_vector)[0]

    btts_confidence = round(
        max(btts_probability) * 100,
        2
    )

    # ==========================
    # CORRECT SCORE AI
    # ==========================

    correct_prediction = correct_score_ai.predict(feature_vector)[0]

    correct_probability = correct_score_ai.predict_proba(feature_vector)[0]

    correct_confidence = round(
        max(correct_probability) * 100,
        2
    )

    correct_score = correct_score_encoder.inverse_transform(
        [correct_prediction]
    )[0]

    print("AI Predictions Completed!")
        # ==========================
    # RESULT MAPS
    # ==========================

    result_map = {
        "H": "🏠 Home Win",
        "D": "🤝 Draw",
        "A": "✈ Away Win"
    }

    goal_map = {
        0: "❌ Under 2.5",
        1: "✅ Over 2.5"
    }

    goal35_map = {
        0: "❌ Under 3.5",
        1: "✅ Over 3.5"
    }

    btts_map = {
        0: "NO",
        1: "YES"
    }

    # ==========================
    # BEST BET
    # ==========================

    best_bet = "Match Result"
    best_confidence = match_confidence

    if over25_confidence > best_confidence:
        best_bet = "Over 2.5"
        best_confidence = over25_confidence

    if over35_confidence > best_confidence:
        best_bet = "Over 3.5"
        best_confidence = over35_confidence

    if btts_confidence > best_confidence:
        best_bet = "BTTS"
        best_confidence = btts_confidence

    # ==========================
    # RETURN RESULTS
    # ==========================

    return {
        "result": result_map.get(match_prediction, match_prediction),
        "confidence": f"{match_confidence} %",
        "goal_market": goal_map[over25_prediction],
        "goal_confidence": f"{over25_confidence} %",
        "goal35": goal35_map[over35_prediction],
        "goal35_confidence": f"{over35_confidence} %",
        "gg": btts_map[btts_prediction],
        "gg_confidence": f"{btts_confidence} %",
        "score": correct_score,
        "score_confidence": f"{correct_confidence} %",
        "bestbet": best_bet,
        "bestbet_confidence": f"{best_confidence} %"
    }
if __name__ == "__main__":
    result = predict_match("Arsenal", "Chelsea")
    print(result)