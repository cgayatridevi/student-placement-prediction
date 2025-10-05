import os
from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "..", "models")

# Load trained model and preprocessing objects
best_model = joblib.load(os.path.join(MODELS_DIR, "best_model.pkl"))
scaler = joblib.load(os.path.join(MODELS_DIR, "scaler.pkl"))
target_encoder = joblib.load(os.path.join(MODELS_DIR, "target_encoder.pkl"))
feature_names = joblib.load(os.path.join(MODELS_DIR, "feature_names.pkl"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        form_data = request.get_json()

        # Binary features mapping
        binary_features = ["ExtracurricularActivities", "PlacementTraining"]

        feature_values = []
        for feature in feature_names:
            value = form_data.get(feature)

            if feature in binary_features:
                # Convert Yes/No to 1/0
                value = 1 if str(value).lower() == "yes" else 0

            try:
                feature_values.append(float(value))
            except (TypeError, ValueError):
                feature_values.append(0.0)

        # Scale features and predict
        features_scaled = scaler.transform(np.array(feature_values).reshape(1, -1))
        prediction = best_model.predict(features_scaled)[0]
        probabilities = best_model.predict_proba(features_scaled)[0]
        prediction_label = target_encoder.inverse_transform([prediction])[0]

        result = {
            "prediction": prediction_label,
            "confidence": round(max(probabilities) * 100, 2),
            "probability_placed": round(probabilities[1] * 100, 2),
            "probability_not_placed": round(probabilities[0] * 100, 2),
            "model_used": type(best_model).__name__
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/about")
def about():
    model_info = {
        "model_type": type(best_model)._name_,
        "features_count": len(feature_names),
        "target_classes": target_encoder.classes_.tolist()
    }
    return render_template("about.html", model_info=model_info)

if __name__ == "__main__":
    app.run(debug=True,port=5000)
