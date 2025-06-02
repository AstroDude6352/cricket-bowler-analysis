# predict_bowler.py
import joblib
import pandas as pd

# Load the trained model
clf = joblib.load("bowler_model.pkl")

# Example input data
input_data = {
    "over_num": 14,
    "balls_left_in_over": 2,
    "overs_left": 5,
    "wickets_left": 5,
    "score": 145,
    "striker_sr": 130.0,
    "non_striker_sr": 115.0
}

df = pd.DataFrame([input_data])
predicted_bowler = clf.predict(df)[0]

print(f"Recommended bowler for this situation: {predicted_bowler}")
