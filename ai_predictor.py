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