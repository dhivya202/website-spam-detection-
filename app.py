from flask import Flask, request, render_template
import joblib
import os
from feature_extraction import extract_features

app = Flask(__name__)

# Load trained ML model
model = joblib.load("spam_model.pkl")


# =========================
# HOME ROUTE
# =========================
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


# =========================
# PREDICTION ROUTE
# =========================
@app.route("/predict", methods=["POST"])
def predict():
    url = request.form["url"]

    # Extract numerical features from URL
    features = extract_features(url)

    # Rule-based spam keywords
    spam_keywords = [
        "free", "win", "offer", "click", "verify", "update",
        "login", "secure", "account", "paypal", "bank"
    ]

    url_lower = url.lower()

    # Hybrid detection: rules + ML
    if (
        any(word in url_lower for word in spam_keywords)
        and (features[2] > 2 or features[0] > 40)
    ):
        result = 1  # Spam
    else:
        result = model.predict([features])[0]

    prediction = "🚨 Spam Website" if result == 1 else "✅ Legitimate Website"

    return render_template(
        "index.html",
        prediction=prediction,
        url=url
    )


# =========================
# REQUIRED FOR RENDER
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.r
