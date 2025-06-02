import json
import pandas as pd
import os

def evaluate_bowler(over_data):
    bowler_stats = {}
    
    for delivery in over_data["deliveries"]:
        bowler = delivery["bowler"]
        runs = delivery["runs"]["total"]
        wickets = len(delivery.get("wickets", []))

        if bowler not in bowler_stats:
            bowler_stats[bowler] = {"runs": 0, "wickets": 0}

        bowler_stats[bowler]["runs"] += runs
        bowler_stats[bowler]["wickets"] += wickets

    # Score = (wickets * 20) - runs
    best_bowler = None
    best_score = float("-inf")
    for bowler, stats in bowler_stats.items():
        score = (stats["wickets"] * 20) - stats["runs"]
        if score > best_score:
            best_score = score
            best_bowler = bowler

    return best_bowler

def process_match_file(filepath):
    with open(filepath) as f:
        data = json.load(f)

    innings = data["innings"]
    rows = []

    for inning in innings:
        team = inning["team"]
        overs = inning["overs"]

        total_score = 0
        total_wickets = 0

        for over in overs:
            over_num = over["over"]
            balls_left_in_over = 6 - len(over["deliveries"])
            overs_left = 20 - (over_num + 1)

            batters = {}
            striker = over["deliveries"][0]["batter"]
            non_striker = over["deliveries"][0]["non_striker"]

            for d in over["deliveries"]:
                b = d["batter"]
                if b not in batters:
                    batters[b] = {"runs": 0, "balls": 0}
                batters[b]["runs"] += d["runs"]["batter"]
                batters[b]["balls"] += 1
                total_score += d["runs"]["total"]
                if "wickets" in d:
                    total_wickets += len(d["wickets"])

            def sr(name):
                if name in batters and batters[name]["balls"] > 0:
                    return (batters[name]["runs"] / batters[name]["balls"]) * 100
                return 0

            striker_sr = sr(striker)
            non_striker_sr = sr(non_striker)

            best_bowler = evaluate_bowler(over)

            rows.append({
                "over_num": over_num,
                "balls_left_in_over": balls_left_in_over,
                "overs_left": overs_left,
                "wickets_left": 10 - total_wickets,
                "score": total_score,
                "striker_sr": striker_sr,
                "non_striker_sr": non_striker_sr,
                "best_bowler": best_bowler
            })

    return rows

# === Process all JSON files in folder ===
data_dir = "dataset/ipl_male_json"  # Folder with your match JSON files
all_data = []

for filename in os.listdir(data_dir):
    if filename.endswith(".json"):
        print("Processing:", filename)
        filepath = os.path.join(data_dir, filename)
        print(f"Processing: {filename}")
        all_data.extend(process_match_file(filepath))

# Create DataFrame and save
df = pd.DataFrame(all_data)
df.to_csv("labeled_training_data.csv", index=False)
print(f"Labeled training data saved. Total samples: {len(df)}")
