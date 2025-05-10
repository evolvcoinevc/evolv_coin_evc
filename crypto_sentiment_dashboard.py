import tweepy
from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# === 1. TWITTER API KEYS (UZUPEŁNIJ SWOIMI DANYMI) ===
API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_API_SECRET"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
ACCESS_SECRET = "YOUR_ACCESS_SECRET"

# === 2. KONFIGURACJA AUTORYZACJI ===
def twitter_auth():
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    return tweepy.API(auth, wait_on_rate_limit=True)

# === 3. POBIERANIE TWEETÓW ===
def fetch_tweets(api, query, count=100):
    tweets = tweepy.Cursor(api.search_tweets, q=query, lang="en", tweet_mode='extended').items(count)
    tweet_list = []
    for tweet in tweets:
        full_text = tweet.full_text
        tweet_list.append(full_text)
    return tweet_list

# === 4. ANALIZA SENTYMENTU ===
def analyze_sentiment(tweets):
    results = []
    for tweet in tweets:
        analysis = TextBlob(tweet)
        polarity = analysis.sentiment.polarity
        sentiment = "positive" if polarity > 0 else "negative" if polarity < 0 else "neutral"
        results.append({"tweet": tweet, "polarity": polarity, "sentiment": sentiment})
    return pd.DataFrame(results)

# === 5. WIZUALIZACJA WYNIKÓW ===
def visualize_results(df, output_dir="output"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    sentiment_counts = df['sentiment'].value_counts()
    colors = ['green' if s == 'positive' else 'red' if s == 'negative' else 'gray' for s in sentiment_counts.index]

    plt.figure(figsize=(8, 5))
    sentiment_counts.plot(kind='bar', color=colors)
    plt.title("Crypto Sentiment Analysis")
    plt.xlabel("Sentiment")
    plt.ylabel("Number of Tweets")
    plt.xticks(rotation=0)
    filename = os.path.join(output_dir, f"sentiment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    plt.tight_layout()
    plt.savefig(filename)
    print(f"[INFO] Wykres zapisany jako: {filename}")

# === 6. URUCHOMIENIE GŁÓWNEJ FUNKCJI ===
def main():
    api = twitter_auth()
    query = "$BTC OR $ETH OR $EVC OR crypto"
    print(f"[INFO] Pobieranie tweetów dla zapytania: {query}")
    tweets = fetch_tweets(api, query, count=200)
    print(f"[INFO] Liczba pobranych tweetów: {len(tweets)}")
    df = analyze_sentiment(tweets)
    print("[INFO] Przykładowe wyniki:")
    print(df.head())
    visualize_results(df)

if __name__ == "__main__":
    main()
