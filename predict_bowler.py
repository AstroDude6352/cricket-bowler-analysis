import joblib
import pandas as pd

def get_float_input(prompt, min_val=None, max_val=None):
    while True:
        try:
            val = float(input(prompt))
            if (min_val is not None and val < min_val) or (max_val is not None and val > max_val):
                print(f"Please enter a value between {min_val} and {max_val}.")
                continue
            return val
        except ValueError:
            print("Invalid input, please enter a number.")

def get_int_input(prompt, min_val=None, max_val=None):
    while True:
        try:
            val = int(input(prompt))
            if (min_val is not None and val < min_val) or (max_val is not None and val > max_val):
                print(f"Please enter an integer between {min_val} and {max_val}.")
                continue
            return val
        except ValueError:
            print("Invalid input, please enter an integer.")

def normalize_name(full_name):
    # full_name example: "KG Williamson"
    parts = full_name.split()
    if len(parts) < 2:
        return full_name  # fallback, just use as is
    first_initial = parts[0][0]  # first letter of first name part
    last_name = parts[-1]
    return f"{first_initial} {last_name}"

def recommend_bowler(clf, le_bowler, df_input, available_bowlers_norm):
    proba = clf.predict_proba(df_input)[0]  # probabilities for each bowler
    classes = le_bowler.classes_

    # Create a map normalized_name -> full_name
    norm_to_full = {normalize_name(c): c for c in classes}

    # Find full names for available bowlers based on normalized input
    matched_bowlers = [norm_to_full[b] for b in available_bowlers_norm if b in norm_to_full]

    if not matched_bowlers:
        print("Warning: None of the provided bowlers match the model's known bowlers.")
        return None

    # Get indices of matched bowlers in model classes
    matched_indices = [i for i, bowler in enumerate(classes) if bowler in matched_bowlers]

    # Pick the matched bowler with highest predicted probability
    best_idx = max(matched_indices, key=lambda i: proba[i])
    return classes[best_idx]

def main():
    clf = joblib.load("bowler_model.pkl")
    le_bowler = joblib.load("label_encoder.pkl")

    print("Enter match situation details:")

    over_num = get_int_input("Over number (0-19): ", 0, 19)
    balls_left_in_over = get_int_input("Balls left in the current over (0-6): ", 0, 6)
    overs_left = get_int_input("Overs left in the innings (0-20): ", 0, 20)
    wickets_left = get_int_input("Wickets left (0-10): ", 0, 10)
    score = get_int_input("Current team score: ", 0)
    striker_sr = get_float_input("Striker strike rate: ", 0)
    non_striker_sr = get_float_input("Non-striker strike rate: ", 0)

    print("\nEnter the current bowling team bowlers as comma-separated names, using first initial and last name format (e.g., K Williamson, J Bumrah):")
    available_bowlers_input = input("Bowling team bowlers: ")
    available_bowlers_norm = [b.strip() for b in available_bowlers_input.split(",") if b.strip()]

    input_data = {
        "over_num": over_num,
        "balls_left_in_over": balls_left_in_over,
        "overs_left": overs_left,
        "wickets_left": wickets_left,
        "score": score,
        "striker_sr": striker_sr,
        "non_striker_sr": non_striker_sr
    }
    df = pd.DataFrame([input_data])

    predicted_bowler = recommend_bowler(clf, le_bowler, df, available_bowlers_norm)
    if predicted_bowler:
        print(f"\nRecommended bowler for this situation (from your team): {predicted_bowler}")
    else:
        print("\nCould not recommend a bowler because none of the provided bowlers are in the model's classes.")

if __name__ == "__main__":
    main()
