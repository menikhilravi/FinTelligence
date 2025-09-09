# --- Tickers to track ---
TICKERS = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]

# --- Database Configuration ---
DB_FILE = "sentiments.db"

# --- Analysis Model ---
# Options: "vader" or "finbert" (if you install pytorch/transformers)
ANALYSIS_MODEL = "vader"

# --- Data Acquisition ---
NUM_HEADLINES = 50  # Number of headlines to fetch per source

# A dictionary of RSS feeds. The {ticker} will be replaced by the actual stock symbol.
# This list has been updated for better reliability.
RSS_FEEDS = {
    "Yahoo Finance": "https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US",
    "MarketWatch": "https://www.marketwatch.com/investing/stock/{ticker}/rss",
    "Finviz": "https://finviz.com/quote.ashx?t={ticker}"
}
