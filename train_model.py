import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.multiclass import unique_labels
import time
import joblib

print("Loading data from CSV...")
df = pd.read_csv("labeled_training_data.csv")
print(f"Data loaded. Shape: {df.shape}")
print("Sample rows:\n", df.head())

print("\nEncoding target column 'best_bowler'...")
le_bowler = LabelEncoder()
df['best_bowler_encoded'] = le_bowler.fit_transform(df['best_bowler'])
print(f"Encoded classes: {list(le_bowler.classes_)}")
print("Encoded target sample:\n", df[['best_bowler', 'best_bowler_encoded']].head())

print("\nPreparing features and target variables...")
X = df.drop(columns=["best_bowler", "best_bowler_encoded"])
y = df['best_bowler_encoded']
print(f"Feature columns: {list(X.columns)}")
print(f"Number of samples: {len(y)}")

print("\nSplitting data into train and test sets...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Training samples: {len(X_train)}, Testing samples: {len(X_test)}")

print("\nInitializing Logistic Regression model...")
model = LogisticRegression(max_iter=200, verbose=1, n_jobs=-1)

print("Starting model training...")
start_time = time.time()
model.fit(X_train, y_train)
print(f"Training completed in {time.time() - start_time:.2f} seconds")

# Save the trained model and label encoder
joblib.dump(model, "bowler_model.pkl")
print("Model saved to 'bowler_model.pkl'")

joblib.dump(le_bowler, "label_encoder.pkl")
print("Label encoder saved to 'label_encoder.pkl'")

print("\nPredicting on test set...")
y_pred = model.predict(X_test)

print("\nCalculating accuracy and generating classification report...")
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.4f}")

labels = unique_labels(y_test, y_pred)
print(f"Labels in test data and predictions: {labels}")
print("Corresponding class names:", le_bowler.inverse_transform(labels))

print("\nClassification Report:")
print(classification_report(y_test, y_pred, labels=labels, target_names=le_bowler.inverse_transform(labels)))
