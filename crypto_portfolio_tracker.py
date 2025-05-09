
import json
import random
import time
from datetime import datetime
import matplotlib.pyplot as plt

class CryptoAsset:
    def __init__(self, symbol, amount):
        self.symbol = symbol.upper()
        self.amount = amount
        self.price_history = []
        self.current_price = 0

    def update_price(self, price):
        self.current_price = price
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.price_history.append((timestamp, price))

    def value(self):
        return self.amount * self.current_price

class Portfolio:
    def __init__(self):
        self.assets = {}

    def add_asset(self, symbol, amount):
        symbol = symbol.upper()
        if symbol in self.assets:
            self.assets[symbol].amount += amount
        else:
            self.assets[symbol] = CryptoAsset(symbol, amount)

    def update_prices(self, price_dict):
        for symbol, asset in self.assets.items():
            if symbol in price_dict:
                asset.update_price(price_dict[symbol])

    def total_value(self):
        return sum(asset.value() for asset in self.assets.values())

    def summary(self):
        print("\nPortfolio Summary:")
        for asset in self.assets.values():
            print(f"{asset.symbol}: {asset.amount} @ ${asset.current_price:.2f} = ${asset.value():.2f}")
        print(f"Total Portfolio Value: ${self.total_value():.2f}\n")

    def plot_price_history(self):
        for asset in self.assets.values():
            if asset.price_history:
                times, prices = zip(*asset.price_history)
                plt.plot(times, prices, label=asset.symbol)
        plt.xlabel("Time")
        plt.ylabel("Price (USD)")
        plt.title("Crypto Price History")
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

def simulate_price_fetch(symbols):
    return {symbol: round(random.uniform(0.9, 1.1) * 100 + random.randint(0, 500), 2) for symbol in symbols}

def main():
    print("Welcome to the Crypto Portfolio Tracker")
    portfolio = Portfolio()

    # Example setup
    portfolio.add_asset("BTC", 0.05)
    portfolio.add_asset("ETH", 2)
    portfolio.add_asset("SOL", 10)

    iterations = 10
    for _ in range(iterations):
        prices = simulate_price_fetch(portfolio.assets.keys())
        portfolio.update_prices(prices)
        portfolio.summary()
        time.sleep(1)

    # Final visualization
    portfolio.plot_price_history()

if __name__ == "__main__":
    main()
