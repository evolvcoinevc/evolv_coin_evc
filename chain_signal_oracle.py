
import random
import json
import pickle
import os
from sklearn.ensemble import RandomForestClassifier

# === Model Training ===
def train_model():
    X = [
        [100, 0.5, 2],
        [500, 1.5, 5],
        [800, 3.0, 10],
        [200, 0.2, 0],
        [600, 2.0, 7]
    ]
    y = ["bearish", "neutral", "bullish", "bearish", "bullish"]
    model = RandomForestClassifier()
    model.fit(X, y)
    with open("trend_classifier.pkl", "wb") as f:
        pickle.dump(model, f)

# === Load Model ===
def load_model():
    if not os.path.exists("trend_classifier.pkl"):
        train_model()
    with open("trend_classifier.pkl", "rb") as f:
        return pickle.load(f)

# === Fetch On-Chain Data (Mock) ===
def fetch_token_data(token_address):
    return {
        "tx_volume": random.randint(100, 1000),
        "holder_growth": random.uniform(0.1, 5.0),
        "contract_events": random.randint(0, 20)
    }

# === Generate Prediction ===
def generate_prediction(data):
    model = load_model()
    input_vector = [[data["tx_volume"], data["holder_growth"], data["contract_events"]]]
    return model.predict(input_vector)[0]

# === Export Signal ===
def export_signal(token_address, signal):
    record = {
        "token": token_address,
        "signal": signal
    }
    with open("token_signal.json", "w") as f:
        json.dump(record, f, indent=4)

# === Main ===
if __name__ == "__main__":
    token_address = "example_token"
    print("Fetching on-chain data...")
    data = fetch_token_data(token_address)
    print("Generating prediction...")
    signal = generate_prediction(data)
    export_signal(token_address, signal)
    print(f"Signal for {token_address}: {signal}")
    print("Saved to token_signal.json")
