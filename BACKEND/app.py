from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from model import train_model, load_model, DATA_FILE

app = Flask(__name__)
CORS(app)

model, anomaly_model = load_model()

@app.route("/")
def home():
    return "AI Water Usage Backend Running"

@app.route("/add", methods=["POST"])
def add_usage():
    global model, anomaly_model

    data = request.json
    usage = data.get("usage")

    df = pd.read_csv(DATA_FILE)
    df.loc[len(df)] = [usage]
    df.to_csv(DATA_FILE, index=False)

    model, anomaly_model = train_model()

    return jsonify({"message": "Data added & model retrained"})

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    recent = data.get("recent")

    if len(recent) != 3:
        return jsonify({"error": "Provide last 3 usage values"}), 400

    recent_array = np.array(recent).reshape(1, -1)
    prediction = model.predict(recent_array)[0]

    anomaly = anomaly_model.predict([[recent[-1]]])[0]
    status = "Anomaly Detected!" if anomaly == -1 else "Normal Usage"

    return jsonify({
        "prediction": round(float(prediction), 2),
        "status": status
    })

if __name__ == "__main__":
    app.run(debug=True)