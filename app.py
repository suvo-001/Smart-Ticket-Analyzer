from flask import Flask, render_template, request, jsonify
import joblib

app = Flask(__name__)

classifier = joblib.load("model/classifier.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")


def get_support_team(category):

    teams = {
        "Account": "Account Support",
        "Payment": "Billing Support",
        "Delivery": "Delivery Support",
        "Refund": "Refund Support",
        "Technical": "Technical Support",
        "Security": "Security Team"
    }

    return teams.get(category, "General Support")


def get_priority(text):

    high_words = [
        "hacked",
        "hack",
        "stolen",
        "security",
        "urgent",
        "blocked",
        "fraud",
        "unauthorized"
    ]

    medium_words = [
        "failed",
        "error",
        "late",
        "problem",
        "issue",
        "not working",
        "crashing"
    ]

    if any(word in text for word in high_words):
        return "High"

    if any(word in text for word in medium_words):
        return "Medium"

    return "Low"


def get_sentiment(text):

    negative_words = [
        "failed",
        "error",
        "problem",
        "issue",
        "angry",
        "bad",
        "late",
        "crashing",
        "hacked",
        "stolen",
        "not working",
        "cannot",
        "can't",
        "unable"
    ]

    positive_words = [
        "thank",
        "thanks",
        "great",
        "good",
        "happy"
    ]

    if any(word in text for word in negative_words):
        return "Negative"

    if any(word in text for word in positive_words):
        return "Positive"

    return "Neutral"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze_ticket():

    data = request.get_json()

    ticket = data.get("ticket", "").strip()

    if not ticket:

        return jsonify({
            "error": "Please enter a support ticket."
        }), 400


    # TF-IDF
    ticket_tfidf = vectorizer.transform([ticket])


    # ML prediction
    prediction = classifier.predict(ticket_tfidf)[0]


    # Probability
    probabilities = classifier.predict_proba(ticket_tfidf)[0]

    confidence = max(probabilities) * 100


    ticket_lower = ticket.lower()


    # Additional analysis
    support_team = get_support_team(prediction)
    priority = get_priority(ticket_lower)
    sentiment = get_sentiment(ticket_lower)


    return jsonify({

        "category": prediction,

        "confidence": round(confidence, 2),

        "support_team": support_team,

        "priority": priority,

        "sentiment": sentiment

    })


if __name__ == "__main__":
    app.run(debug=True)