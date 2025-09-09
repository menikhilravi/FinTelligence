# database.py

import sqlite3
import pandas as pd
from datetime import datetime


def initialize_db(db_file: str):
    """
    Initializes the SQLite database and creates the 'sentiments' table if it doesn't exist.
    """
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Create table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS sentiments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME NOT NULL,
            ticker TEXT NOT NULL,
            source TEXT NOT NULL,
            text TEXT NOT NULL,
            processed_text TEXT,
            sentiment_label TEXT,
            sentiment_score REAL,
            UNIQUE(ticker, text)
        )
        ''')

        conn.commit()
        conn.close()
        print(f"Database '{db_file}' initialized successfully.")
    except sqlite3.Error as e:
        print(f"Database error during initialization: {e}")


def save_sentiments(df: pd.DataFrame, ticker: str, db_file: str):
    """
    Saves the sentiment data from a DataFrame into the SQLite database.
    Duplicates based on (ticker, text) are ignored.
    """
    if df.empty:
        print("No new data to save.")
        return

    try:
        conn = sqlite3.connect(db_file)

        # Add timestamp and ticker columns
        df_to_save = df.copy()
        df_to_save['timestamp'] = datetime.now()
        df_to_save['ticker'] = ticker

        # Reorder columns to match the table schema
        cols = ['timestamp', 'ticker', 'source', 'text',
                'processed_text', 'sentiment_label', 'sentiment_score']
        df_to_save = df_to_save[cols]

        # Use 'to_sql' with a conflict resolution strategy to ignore duplicates
        # The 'UNIQUE(ticker, text)' constraint in the table is crucial here
        df_to_save.to_sql('sentiments', conn, if_exists='append', index=False)

        conn.close()
        print(
            f"Successfully saved {len(df_to_save)} new entries for {ticker} to the database.")
    except sqlite3.Error as e:
        print(f"Database error during save operation: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during save: {e}")
