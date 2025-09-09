# FinTelligence

Value Proposition

    Core Problem: Financial markets are flooded with unstructured data (news, social media). It's impossible for a human to read and process it all in real-time to gauge market sentiment.

    My Solution: This app will automate the collection and analysis of this data, aggregating it into a simple, actionable sentiment score (e.g., Positive, Negative, Neutral) for specific stocks. This provides a data-driven edge for making investment decisions.

Key Features for a Minimum Viable Product (MVP)

    Stock Ticker Input: A simple interface to enter a stock symbol (e.g., AAPL, TSLA, GOOG).

    Sentiment Score: A clear, real-time sentiment score (e.g., "Bullish").

    Source Tracking: Display the headlines and tweets that influenced the score, so I can verify the data and avoid blind trust in the algorithm. This directly addresses "no hallucination" requirement by grounding the sentiment in factual, verifiable sources.

    Historical View: A simple chart showing how the sentiment score for a stock has changed over the last 24-48 hours.

Risks and Important Disclaimers

    Correlation, not Causation: High positive sentiment does not guarantee a stock price will go up. The market is influenced by countless factors (e.g., earnings reports, federal interest rates, geopolitical events). This tool is one of many potential signals, not a crystal ball.

    Garbage In, Garbage Out: The accuracy of your output is entirely dependent on the quality of your input data. Sarcasm, irony, and complex financial jargon are notoriously difficult for algorithms to understand.

    Legal & Financial Advice: This application is for informational purposes only and should never be considered financial advice. All investment decisions carry risk.


Features

    News Data Acquisition: Fetches news from Yahoo Finance RSS feeds.

    Flexible Sentiment Analysis: Supports two different sentiment analysis models:

        VADER: A fast, lexicon-based model great for general-purpose text.

        FinBERT (Commented out): A powerful, domain-specific transformer model trained on financial text for higher accuracy (requires more setup).

    Local Data Storage: Uses SQLite for a simple, serverless, and robust local database.

    Interactive Dashboard: A web-based UI built with Streamlit to visualize and explore the sentiment data.

    Automated & Configurable: Runs automatically on a schedule and is easily configured via the config.py file.

Project Structure
.
├── config.py               # Configuration file for tickers, API keys, etc.
├── data_acquisition.py     # Module for fetching data from news feeds.
├── sentiment_analysis.py   # Module for text preprocessing and sentiment analysis.
├── database.py             # Module for all SQLite database interactions.
├── main.py                 # Main entry point to run the data collection pipeline.
├── app.py                  # The Streamlit UI dashboard application.
├── requirements.txt        # Lists all Python package dependencies.
└── README.md               # This file.

Setup & Installation

    Clone the Repository
    git clone <repository_url>
    cd <repository_name>

    Create a Virtual Environment
    python -m venv venv
    source ven/bin/activate  # On Windows, use `venv\Scripts\activate`

    Install Dependencies
    pip install -r requirements.txt

Usage

The project has two main parts: the data collection script and the UI dashboard.
1. Run the Data Collector

First, you need to collect some data. Run the main.py script from your terminal. This will fetch headlines, analyze them, and save them to sentiments.db. You can leave this running in a terminal to continuously collect data.

python main.py

2. Launch the UI Dashboard

While the data collector is running (or after it has run at least once), open a new terminal (with the virtual environment activated) and run the following command:

streamlit run app.py

This will launch the interactive dashboard in a new tab in your web browser. You can use the search box or dropdown in the sidebar to explore the sentiment for different tickers.




-- UI & Advanced Features: The "Next Level" -- 

Advanced Key UI Components:

    Interactive charts with Plotly
    Color-coded cards for headlines
    Auto-refreshing data


Advanced Features

Once the MVP is functional these enhancements to improve its capabilities and accuracy.
Potential Upgrades:
    Add more data sources (Reddit, SEC filings)
    Use Named Entity Recognition (NER) for accuracy
    Implement an automated alerting system
    Backtest sentiment against historical prices


