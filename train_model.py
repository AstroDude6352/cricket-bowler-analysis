import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import time

# Load data
df = pd.read_csv("labeled_training_data.csv")

# Encode target 'best_bowler'
le_bowler = LabelEncoder()
df['best_bowler_encoded'] = le_bowler.fit_transform(df['best_bowler'])

# Features and target
X = df.drop(columns=["best_bowler", "best_bowler_encoded"])
y = df['best_bowler_encoded']

# Split data
print("Splitting data into train and test sets...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Training samples: {len(X_train)}, Testing samples: {len(X_test)}")

# Initialize model
model = LogisticRegression(max_iter=200, verbose=1, n_jobs=-1)

print("Starting model training...")
start_time = time.time()

model.fit(X_train, y_train)

print(f"Training completed in {time.time() - start_time:.2f} seconds")

# Predictions
y_pred = model.predict(X_test)

# Metrics
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.4f}")
print("Classification Report:")
print(classification_report(y_test, y_pred, target_names=le_bowler.classes_))
