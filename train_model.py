import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# 1. Load dataset
data = pd.read_csv("dataset/tickets.csv")

# 2. Separate text and category
X = data["text"]
y = data["category"]


# 3. Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# 4. Convert text into TF-IDF
vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english",
    ngram_range=(1, 2)
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)


# 5. Create ML classifier
classifier = LogisticRegression(
    max_iter=1000
)


# 6. Train model
classifier.fit(X_train_tfidf, y_train)


# 7. Make predictions
predictions = classifier.predict(X_test_tfidf)


# 8. Calculate accuracy
accuracy = accuracy_score(y_test, predictions)


print("--------------------------------")
print("SmartTicket AI Model")
print("--------------------------------")

print(f"Training samples: {len(X_train)}")
print(f"Testing samples:  {len(X_test)}")

print("--------------------------------")
print(f"Accuracy: {accuracy * 100:.2f}%")

print("--------------------------------")
print("Classification Report")
print("--------------------------------")

print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)


# 9. Save model
joblib.dump(
    classifier,
    "model/classifier.pkl"
)

joblib.dump(
    vectorizer,
    "model/vectorizer.pkl"
)


print("--------------------------------")
print("Model trained successfully!")
print("Saved:")
print("model/classifier.pkl")
print("model/vectorizer.pkl")