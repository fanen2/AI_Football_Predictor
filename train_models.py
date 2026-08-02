import pandas as pd
import joblib

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

print("=" * 60)
print("AI Football Predictor by Fanen")
print("MASTER AI TRAINING SYSTEM")
print("=" * 60)

# ==========================================
# LOAD DATASET
# ==========================================

print("\nLoading Dataset...")

data = pd.read_csv(
    "/storage/emulated/0/Download/final_ai_dataset.csv"
)

data = data.dropna()

print("Dataset Loaded Successfully!")
print("Total Matches:", len(data))

# ==========================================
# TEAM ENCODER
# ==========================================

print("\nPreparing Team Encoder...")

team_encoder = LabelEncoder()

all_teams = pd.concat([
    data["HomeTeam"],
    data["AwayTeam"]
])

team_encoder.fit(all_teams)

original_data = data.copy()

data["HomeTeam"] = team_encoder.transform(data["HomeTeam"])
data["AwayTeam"] = team_encoder.transform(data["AwayTeam"])

joblib.dump(
    team_encoder,
    "team_encoder.pkl"
)

print("Team Encoder Saved!")

# ==========================================
# COMMON FEATURES
# ==========================================

features = [

    "HomeTeam",
    "AwayTeam",

    "HomeRecentPoints",
    "AwayRecentPoints",

    "HomeWinRate",
    "AwayWinRate",

    "H2HHomeWins",
    "H2HAwayWins",
    "H2HDraws",
    "H2HGoalsAvg",

    "HomeAttackStrength",
    "AwayAttackStrength",

    "HomeDefenseStrength",
    "AwayDefenseStrength",

    "ExpectedHomeGoals",
    "ExpectedAwayGoals"

]

print("\nShared Feature Matrix Ready!")
print("Number of Features:", len(features))
# ==========================================
# TRAIN MATCH RESULT AI
# ==========================================

print("\n" + "=" * 60)
print("TRAINING MATCH RESULT AI")
print("=" * 60)

match_data = data.copy()

result_encoder = LabelEncoder()

match_data["FTR"] = result_encoder.fit_transform(
    match_data["FTR"]
)

X = match_data[features]
y = match_data["FTR"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

match_model = HistGradientBoostingClassifier(
    learning_rate=0.05,
    max_depth=8,
    max_iter=300,
    random_state=42
)

match_model.fit(X_train, y_train)

predictions = match_model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("Match Result Accuracy:",
      round(accuracy * 100, 2),
      "%")

joblib.dump(
    match_model,
    "match_result_ai_v6.pkl"
)

joblib.dump(
    result_encoder,
    "match_result_encoder_v6.pkl"
)

print("Match Result AI Saved!")
# ==========================================
# TRAIN OVER 2.5 AI
# ==========================================

print("\n" + "=" * 60)
print("TRAINING OVER 2.5 GOALS AI")
print("=" * 60)

over25_data = data.copy()

over25_data["Over25"] = (
    (over25_data["FTHG"] + over25_data["FTAG"]) >= 3
).astype(int)

X = over25_data[features]
y = over25_data["Over25"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

over25_model = RandomForestClassifier(
    n_estimators=300,
    max_depth=12,
    random_state=42,
    n_jobs=-1
)

over25_model.fit(X_train, y_train)

predictions = over25_model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("Over 2.5 Accuracy:",
      round(accuracy * 100, 2),
      "%")

joblib.dump(
    over25_model,
    "over25_ai_v1.pkl"
)

print("Over 2.5 AI Saved!")
# ==========================================
# TRAIN OVER 3.5 AI
# ==========================================

print("\n" + "=" * 60)
print("TRAINING OVER 3.5 GOALS AI")
print("=" * 60)

over35_data = data.copy()

over35_data["Over35"] = (
    (over35_data["FTHG"] + over35_data["FTAG"]) >= 4
).astype(int)

X = over35_data[features]
y = over35_data["Over35"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

over35_model = RandomForestClassifier(
    n_estimators=300,
    max_depth=12,
    random_state=42,
    n_jobs=-1
)

over35_model.fit(X_train, y_train)

predictions = over35_model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("Over 3.5 Accuracy:",
      round(accuracy * 100, 2),
      "%")

joblib.dump(
    over35_model,
    "over35_ai_v1.pkl"
)

print("Over 3.5 AI Saved!")
# ==========================================
# TRAIN BTTS AI
# ==========================================

print("\n" + "=" * 60)
print("TRAINING BTTS AI")
print("=" * 60)

btts_data = data.copy()

btts_data["BTTS"] = (
    (btts_data["FTHG"] > 0) &
    (btts_data["FTAG"] > 0)
).astype(int)

X = btts_data[features]
y = btts_data["BTTS"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

btts_model = RandomForestClassifier(
    n_estimators=300,
    max_depth=12,
    random_state=42,
    n_jobs=-1
)

btts_model.fit(X_train, y_train)

predictions = btts_model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("BTTS Accuracy:",
      round(accuracy * 100, 2),
      "%")

joblib.dump(
    btts_model,
    "btts_ai_v1.pkl"
)

print("BTTS AI Saved!")
# ==========================================
# TRAIN CORRECT SCORE AI
# ==========================================

print("\n" + "=" * 60)
print("TRAINING CORRECT SCORE AI")
print("=" * 60)

score_data = original_data.copy()

score_data["CorrectScore"] = (
    score_data["FTHG"].astype(int).astype(str)
    + "-"
    + score_data["FTAG"].astype(int).astype(str)
)

top_scores = (
    score_data["CorrectScore"]
    .value_counts()
    .head(15)
)

score_data = score_data[
    score_data["CorrectScore"].isin(top_scores.index)
].reset_index(drop=True)

# Encode teams again
score_data["HomeTeam"] = team_encoder.transform(
    score_data["HomeTeam"]
)

score_data["AwayTeam"] = team_encoder.transform(
    score_data["AwayTeam"]
)

score_encoder = LabelEncoder()

score_data["ScoreLabel"] = score_encoder.fit_transform(
    score_data["CorrectScore"]
)

X = score_data[features]
y = score_data["ScoreLabel"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

correct_model = RandomForestClassifier(
    n_estimators=150,
    max_depth=10,
    random_state=42,
    n_jobs=-1
)

correct_model.fit(X_train, y_train)

predictions = correct_model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("Correct Score Accuracy:",
      round(accuracy * 100, 2),
      "%")

joblib.dump(
    correct_model,
    "correct_score_ai_v2.pkl"
)

joblib.dump(
    score_encoder,
    "correct_score_encoder_v2.pkl"
)

print("Correct Score AI Saved!")
print("Correct Score Encoder Saved!")

print("\n" + "=" * 60)
print("ALL AI MODELS TRAINED SUCCESSFULLY!")
print("=" * 60)