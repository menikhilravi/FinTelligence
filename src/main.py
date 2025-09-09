# main.py

import time
import pandas as pd
from data_acquisition import get_data
from sentiment_analysis import analyze_dataframe
from database import initialize_db, save_sentiments
import config


def run_pipeline():
    """
    Executes one full run of the data pipeline for all tickers.
    """
    print("--- Starting Stock Sentiment Pipeline ---")

    for ticker in config.TICKERS:
        print(f"\n--- Processing ticker: {ticker} ---")

        # 1. Data Acquisition
        raw_data_df = get_data(
            ticker=ticker,
            num_headlines=config.NUM_HEADLINES
        )

        if raw_data_df.empty:
            print(f"No data collected for {ticker}. Skipping...")
            continue

        # 2. Sentiment Analysis
        analyzed_df = analyze_dataframe(
            df=raw_data_df,
            model_type=config.ANALYSIS_MODEL
        )

        # 3. Data Storage
        save_sentiments(
            df=analyzed_df,
            ticker=ticker,
            db_file=config.DB_FILE
        )

    print("\n--- Pipeline run finished. ---")


if __name__ == "__main__":
    # Initialize the database on the first run
    initialize_db(config.DB_FILE)

    # Run the pipeline in a loop
    while True:
        run_pipeline()
        print(f"Sleeping for {config.SLEEP_INTERVAL} seconds...")
        time.sleep(config.SLEEP_INTERVAL)
