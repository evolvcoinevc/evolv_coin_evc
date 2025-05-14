import random
import time
from typing import Dict

# Symulowane dane tokenów
TOKENS = ["EVC", "SOL", "ETH", "BTC"]
INITIAL_BALANCE = 10000

class Portfolio:
    def __init__(self):
        self.balances = {token: 0 for token in TOKENS}
        self.cash = INITIAL_BALANCE

    def buy(self, token: str, amount: float, price: float):
        cost = amount * price
        if self.cash >= cost:
            self.balances[token] += amount
            self.cash -= cost
            print(f"BUY {amount:.2f} {token} @ {price:.2f} | Cash: {self.cash:.2f}")
        else:
            print("Not enough cash to buy.")

    def sell(self, token: str, amount: float, price: float):
        if self.balances[token] >= amount:
            self.balances[token] -= amount
            self.cash += amount * price
            print(f"SELL {amount:.2f} {token} @ {price:.2f} | Cash: {self.cash:.2f}")
        else:
            print("Not enough token to sell.")

    def value(self, prices: Dict[str, float]):
        total = self.cash
        for token, amount in self.balances.items():
            total += amount * prices[token]
        return total

class Market:
    def __init__(self):
        self.prices = {token: random.uniform(10, 1000) for token in TOKENS}

    def update_prices(self):
        for token in TOKENS:
            change = random.uniform(-0.05, 0.05)
            self.prices[token] *= (1 + change)
        return self.prices

def get_sentiment_score(token: str) -> float:
    return random.uniform(-1, 1)

def get_chain_signal(token: str) -> float:
    return random.uniform(-1, 1)

class TradingAgent:
    def __init__(self, portfolio: Portfolio, market: Market):
        self.portfolio = portfolio
        self.market = market

    def evaluate(self):
        prices = self.market.update_prices()
        for token in TOKENS:
            sentiment = get_sentiment_score(token)
            signal = get_chain_signal(token)
            score = sentiment * 0.5 + signal * 0.5

            price = prices[token]
            decision_threshold = 0.3
            amount = random.uniform(0.5, 2.0)

            if score > decision_threshold:
                self.portfolio.buy(token, amount, price)
            elif score < -decision_threshold:
                self.portfolio.sell(token, amount, price)
            else:
                print(f"HOLD {token} | Score: {score:.2f}")

        total = self.portfolio.value(prices)
        print(f"Portfolio Value: {total:.2f}\n")

def run_simulation(rounds: int = 10, delay: float = 1.0):
    market = Market()
    portfolio = Portfolio()
    agent = TradingAgent(portfolio, market)

    for round in range(rounds):
        print(f"--- Round {round + 1} ---")
        agent.evaluate()
        time.sleep(delay)

if __name__ == "__main__":
    run_simulation()
