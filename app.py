import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from transformers import pipeline
from datetime import datetime, timedelta
import time

app = Flask(__name__)
CORS(app)

# --- Configuration ---
FINNHUB_API_KEY = " d2evropr01qmrq4p4ulgd2evropr01qmrq4p4um0" # Make sure your key is here!
FINNHUB_BASE_URL = "https://finnhub.io/api/v1"

# --- Initialize Sentiment Analysis Pipeline ---
sentiment_pipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert")

# --- API Helper Functions ---
def fetch_finnhub_data(endpoint, params={}):
    params['token'] = FINNHUB_API_KEY
    try:
        response = requests.get(f"{FINNHUB_BASE_URL}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {endpoint}: {e}")
        return None

# --- Main API Endpoint ---
@app.route("/api/stock/<string:ticker>")
def get_stock_data(ticker):
    # This endpoint remains the same, fetching profile, quote, and news
    profile = fetch_finnhub_data('stock/profile2', {'symbol': ticker})
    if not profile:
        return jsonify({"error": "Could not fetch company profile. Invalid ticker?"}), 404
    quote = fetch_finnhub_data('quote', {'symbol': ticker})
    if not quote:
        return jsonify({"error": "Could not fetch stock quote."}), 500
    
    today = datetime.now()
    one_month_ago = today - timedelta(days=30)
    news_data = fetch_finnhub_data('company-news', {
        'symbol': ticker,
        'from': one_month_ago.strftime('%Y-%m-%d'),
        'to': today.strftime('%Y-%m-%d')
    })
    analyzed_news = []
    if news_data:
        for item in news_data[:10]:
            if item['headline']:
                sentiment = sentiment_pipeline([item['headline']])[0]
                analyzed_news.append({
                    'headline': item['headline'], 'url': item['url'], 
                    'summary': item['summary'], 'source': item['source'], 
                    'sentiment': sentiment
                })
    consolidated_data = {
        'profile': profile, 'quote': quote, 'news': analyzed_news
    }
    return jsonify(consolidated_data)

# --- ✨ NEW ENDPOINT FOR CHART DATA ✨ ---
@app.route("/api/stock/history/<string:ticker>")
def get_stock_history(ticker):
    resolution = request.args.get('resolution', 'D') # Default to daily
    
    # Calculate 'from' and 'to' timestamps
    to_timestamp = int(time.time())
    from_timestamp = to_timestamp - (365 * 24 * 60 * 60) # Default to 1 year back

    # Override 'from' based on a 'range' query parameter
    time_range = request.args.get('range', '1y')
    if time_range == '1m':
        from_timestamp = to_timestamp - (30 * 24 * 60 * 60)
    elif time_range == '6m':
        from_timestamp = to_timestamp - (180 * 24 * 60 * 60)
    
    history_data = fetch_finnhub_data('stock/candle', {
        'symbol': ticker,
        'resolution': resolution,
        'from': from_timestamp,
        'to': to_timestamp
    })
    
    if not history_data or history_data.get('s') == 'no_data':
        return jsonify({"error": "Could not fetch historical data."}), 404
        
    return jsonify(history_data)

# --- Run the App ---
if __name__ == "__main__":
    app.run(debug=True, port=5000)