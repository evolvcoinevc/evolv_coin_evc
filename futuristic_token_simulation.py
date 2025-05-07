
# futuristic_token_simulation.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import random
import string
import datetime

# =====================
# CONFIG
# =====================
NUM_TOKENS = 100
SIM_DAYS = 100
SEED = 42
np.random.seed(SEED)
random.seed(SEED)

# =====================
# UTILS
# =====================
def random_token_name():
    return ''.join(random.choices(string.ascii_uppercase, k=4)) + str(random.randint(10, 99))

def generate_ai_traits():
    return {
        'ai_power': np.clip(np.random.normal(0.7, 0.2), 0, 1),
        'eco_impact': np.clip(np.random.normal(0.5, 0.3), 0, 1),
        'adoption_rate': np.clip(np.random.normal(0.6, 0.2), 0, 1),
        'hype_index': np.clip(np.random.normal(0.5, 0.4), 0, 1)
    }

# =====================
# TOKEN CLASS
# =====================
class FuturisticToken:
    def __init__(self, name):
        self.name = name
        self.traits = generate_ai_traits()
        self.initial_price = round(1 + 10 * self.traits['hype_index'], 2)
        self.price_history = [self.initial_price]

    def simulate_day(self):
        last_price = self.price_history[-1]
        volatility = (0.01 + 0.05 * self.traits['hype_index'])
        news_impact = np.random.normal(0, volatility)
        trait_score = sum(self.traits.values()) / len(self.traits)
        growth = 0.01 * trait_score
        new_price = max(0.1, last_price * (1 + growth + news_impact))
        self.price_history.append(round(new_price, 4))

# =====================
# MARKET SIMULATION
# =====================
def simulate_market(tokens, days):
    for _ in range(days):
        for token in tokens:
            token.simulate_day()

def create_market():
    return [FuturisticToken(random_token_name()) for _ in range(NUM_TOKENS)]

# =====================
# ML PREDICTION
# =====================
def train_predict_model(token: FuturisticToken):
    data = pd.DataFrame({
        'day': list(range(len(token.price_history))),
        'price': token.price_history
    })
    data['prev_price'] = data['price'].shift(1).fillna(method='bfill')
    
    X = data[['day', 'prev_price']]
    y = data['price']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"[ML] {token.name} - MSE: {mse:.4f}")

    # Predict next 5 days
    last_day = data['day'].iloc[-1]
    last_price = data['price'].iloc[-1]
    future_days = []
    for i in range(1, 6):
        day = last_day + i
        pred = model.predict([[day, last_price]])[0]
        future_days.append((day, pred))
        last_price = pred

    return future_days

# =====================
# STRATEGY (Buy Low, Predict High)
# =====================
def find_best_investment(tokens):
    best_gain = 0
    best_token = None
    for token in tokens:
        predictions = train_predict_model(token)
        current_price = token.price_history[-1]
        future_price = predictions[-1][1] if predictions else current_price
        gain = (future_price - current_price) / current_price
        if gain > best_gain:
            best_gain = gain
            best_token = (token, current_price, future_price)

    return best_token

# =====================
# VISUALIZATION
# =====================
def plot_token(token: FuturisticToken):
    plt.figure(figsize=(10, 4))
    plt.plot(token.price_history, label=token.name)
    plt.title(f"Token: {token.name} - Final Price: {token.price_history[-1]:.2f}")
    plt.xlabel("Day")
    plt.ylabel("Price")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# =====================
# MAIN EXECUTION
# =====================
if __name__ == '__main__':
    print("[SIM] Generating market...")
    market = create_market()
    
    print(f"[SIM] Simulating {SIM_DAYS} days of trading...")
    simulate_market(market, SIM_DAYS)

    print("[STRATEGY] Analyzing best performing token...")
    best = find_best_investment(market)
    if best:
        token, price_now, predicted = best
        print(f"\n[RESULT] Best Token: {token.name}")
        print(f"Current Price: {price_now:.2f}, Predicted in 5 days: {predicted:.2f}")
        plot_token(token)
    else:
        print("[RESULT] No viable token found.")
