import joblib

# Load trained model
classifier = joblib.load("model/classifier.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")

# Test tickets
tickets = [
    "I forgot my password",
    "My payment was deducted but order failed",
    "My package has not arrived",
    "I want my money back",
    "The application keeps crashing",
    "Someone hacked my account"
]

for ticket in tickets:

    # Convert ticket text into TF-IDF
    ticket_tfidf = vectorizer.transform([ticket])

    # Predict category
    prediction = classifier.predict(ticket_tfidf)

    # Get confidence
    probabilities = classifier.predict_proba(ticket_tfidf)
    confidence = max(probabilities[0]) * 100

    print("--------------------------------")
    print("Ticket:", ticket)
    print("Category:", prediction[0])
    print(f"Confidence: {confidence:.2f}%")