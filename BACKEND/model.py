import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest
import joblib

MODEL_FILE = "water_model.pkl"
ANOMALY_FILE = "anomaly_model.pkl"
DATA_FILE = "data.csv"

def train_model():
    df = pd.read_csv(DATA_FILE)

    if len(df) < 4:
        return None, None

    X = []
    y = []

    for i in range(3, len(df)):
        X.append(df["usage"][i-3:i].values)
        y.append(df["usage"][i])

    X = np.array(X)
    y = np.array(y)

    model = LinearRegression()
    model.fit(X, y)

    anomaly_model = IsolationForest(contamination=0.1)
    anomaly_model.fit(df[["usage"]])

    joblib.dump(model, MODEL_FILE)
    joblib.dump(anomaly_model, ANOMALY_FILE)

    return model, anomaly_model

def load_model():
    try:
        model = joblib.load(MODEL_FILE)
        anomaly_model = joblib.load(ANOMALY_FILE)
        return model, anomaly_model
    except:
        return train_model()