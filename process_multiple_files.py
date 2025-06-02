import os
import json
import pandas as pd
from data_extraction import extract_features  # or the function you use to process 1 file

folder_path = "ipl_male_json"  # update this to your folder

all_dataframes = []

for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        file_path = os.path.join(folder_path, filename)
        print(f"Processing {filename}...")

        with open(file_path) as f:
            data = json.load(f)

        # Assuming you have a function that processes one JSON and returns a DataFrame:
        df = extract_features(data)
        all_dataframes.append(df)

# Combine all DataFrames
combined_df = pd.concat(all_dataframes, ignore_index=True)

# Save combined data to CSV for training
combined_df.to_csv("combined_training_data.csv", index=False)
print("Combined training data saved.")
