from flask import Flask, jsonify, render_template
from flask_cors import CORS
import requests
import yfinance as yf

app = Flask(__name__)
CORS(app)

# Free APIs for news and crypto prices
NEWS_API_URL = "https://newsapi.org/v2/top-headlines?category=business&apiKey=YOUR_NEWS_API_KEY"
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"

def get_news():
    """Fetch latest stock market & crypto news"""
    try:
        response = requests.get(NEWS_API_URL)
        news_data = response.json().get("articles", [])[:5]  # Get top 5 news headlines
        return [{"title": article["title"], "url": article["url"]} for article in news_data]
    except Exception as e:
        return [{"title": "Error fetching news", "url": "#"}]

def get_crypto_prices():
    """Fetch latest cryptocurrency prices"""
    try:
        response = requests.get(COINGECKO_API_URL)
        data = response.json()
        return {
            "Bitcoin": f"${data['bitcoin']['usd']}",
            "Ethereum": f"${data['ethereum']['usd']}"
        }
    except:
        return {"Bitcoin": "Error", "Ethereum": "Error"}

def get_stock_prices():
    """Fetch latest stock prices (Example: Apple & Tesla)"""
    try:
        stocks = ["AAPL", "TSLA"]
        prices = {stock: f"${yf.Ticker(stock).history(period='1d')['Close'].iloc[-1]:.2f}" for stock in stocks}
        return prices
    except:
        return {"AAPL": "Error", "TSLA": "Error"}

@app.route("/")
def home():
    """Render the ticker webpage"""
    return render_template("index.html")

@app.route("/api/news")
def news():
    """API endpoint for fetching news"""
    return jsonify(get_news())

@app.route("/api/prices")
def prices():
    """API endpoint for fetching stock & crypto prices"""
    return jsonify({
        "stocks": get_stock_prices(),
        "crypto": get_crypto_prices()
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
