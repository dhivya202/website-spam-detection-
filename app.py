from flask import Flask, request, render_template
import joblib
from feature_extraction import extract_features

# Create Flask app
app = Flask(__name__)

# Load trained ML model
model = joblib.load("spam_model.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    # Get URL from user
    url = request.form["url"]

    # Extract numerical features from URL
    features = extract_features(url)

    # Spam-related keywords (phishing & scam words)
    spam_keywords = [
        "free", "win", "offer", "click", "verify", "update",
        "login", "secure", "account", "paypal", "bank"
    ]

    url_lower = url.lower()

    # Hybrid detection: rule-based + ML
    if (
        any(word in url_lower for word in spam_keywords)
        and (features[2] > 2 or features[0] > 40)
    ):
        result = 1   # Spam
    else:
        result = model.predict([features])[0]

    # Final output
    prediction = "🚨 Spam Website" if result == 1 else "✅ Legitimate Website"

    return render_template(
        "index.html",
        prediction=prediction,
        url=url
    )


if __name__ == "__main__":
    app.run(debug=True)
