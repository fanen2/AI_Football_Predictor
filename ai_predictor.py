import pandas as pd
import numpy as np
import joblib

from sklearn.preprocessing import LabelEncoder

from team_name_mapper import TEAM_MAP
print("Loading AI Prediction Engine...")

# Load Dataset
data = pd.read_csv(
    "/storage/emulated/0/Download/final_ai_dataset.csv"
)

# Load Models
match_ai = joblib.load(
    "/storage/emulated/0/Download/match_result_ai_v6.pkl"
)

match_result_encoder = joblib.load(
    "/storage/emulated/0/Download/match_result_encoder_v6.pkl"
)

over25_ai = joblib.load(
    "/storage/emulated/0/Download/over25_ai_v1.pkl"
)

over35_ai = joblib.load(
    "/storage/emulated/0/Download/over35_ai_v1.pkl"
)

btts_ai = joblib.load(
    "/storage/emulated/0/Download/btts_ai_v1.pkl"
)

correct_score_ai = joblib.load(
    "/storage/emulated/0/Download/correct_score_ai_v2.pkl"
)

correct_score_encoder = joblib.load(
    "/storage/emulated/0/Download/correct_score_encoder_v2.pkl"
)

print("AI Models Loaded Successfully!")
print("Preparing Team Encoder...")

team_encoder = LabelEncoder()

all_teams = pd.concat([
    data["HomeTeam"],
    data["AwayTeam"]
])

team_encoder.fit(all_teams)

print("Team Encoder Ready!")
def predict_match(home_team, away_team):

    print("===================================")
    print("Starting AI Prediction...")
    print(home_team, "vs", away_team)
    print("===================================")
def predict_match(home_team, away_team):

    print("===================================")
    print("Starting AI Prediction...")
    print(home_team, "vs", away_team)
    print("===================================")

    # Map Team Names
    home_team = TEAM_MAP.get(home_team, home_team)
    away_team = TEAM_MAP.get(away_team, away_team)

    print("Mapped Teams:")
    print(home_team, "vs", away_team)

    # Load Latest Team Records
    home_record = data[
        data["HomeTeam"] == home_team
    ].iloc[-1]

    away_record = data[
        data["AwayTeam"] == away_team
    ].iloc[-1]

    print("Historical Data Loaded Successfully!")
print("Historical Data Loaded Successfully!")
print("Building AI Feature Vector...")

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
print("Feature Vector Created Successfully!")
print("Running AI Models...")

# Match Result
match_prediction = match_ai.predict(feature_vector)[0]
match_prediction = match_result_encoder.inverse_transform(
    [match_prediction]
)[0]
match_probability = match_ai.predict_proba(feature_vector)[0]
match_confidence = round(max(match_probability) * 100, 2)

# Over 2.5
over25_prediction = over25_ai.predict(feature_vector)[0]
over25_probability = over25_ai.predict_proba(feature_vector)[0]
over25_confidence = round(max(over25_probability) * 100, 2)

# Over 3.5
over35_prediction = over35_ai.predict(feature_vector)[0]
over35_probability = over35_ai.predict_proba(feature_vector)[0]
over35_confidence = round(max(over35_probability) * 100, 2)

# BTTS
btts_prediction = btts_ai.predict(feature_vector)[0]
btts_probability = btts_ai.predict_proba(feature_vector)[0]
btts_confidence = round(max(btts_probability) * 100, 2)

# Correct Score
correct_prediction = correct_score_ai.predict(feature_vector)[0]
correct_probability = correct_score_ai.predict_proba(feature_vector)[0]
correct_confidence = round(max(correct_probability) * 100, 2)

correct_score = correct_score_encoder.inverse_transform(
    [correct_prediction]
)[0]

print("AI Prediction Completed!")