# sentiment_analysis.py

import pandas as pd
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Note: Using FinBERT requires installing PyTorch or TensorFlow
# from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# --- Text Preprocessing ---


def preprocess_text(text: str) -> str:
    """
    Cleans and preprocesses a single string of text.
    - Converts to lowercase
    - Removes URLs, mentions, and hashtags
    - Removes special characters and numbers
    """
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text,
                  flags=re.MULTILINE)  # Remove URLs
    text = re.sub(r'\@\w+|\#', '', text)  # Remove mentions and hashtags
    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = " ".join(text.split())  # Remove extra whitespace
    return text

# --- VADER Sentiment Analysis ---


def analyze_sentiment_vader(text: str) -> float:
    """
    Analyzes sentiment of a text using VADER.

    Args:
        text (str): The preprocessed text to analyze.

    Returns:
        float: The compound sentiment score from -1 (negative) to 1 (positive).
    """
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(text)
    return sentiment['compound']

# --- FinBERT Sentiment Analysis (Advanced) ---
# class FinbertAnalyzer:
#     """A class to handle FinBERT analysis to avoid reloading the model."""
#     def __init__(self):
#         print("Initializing FinBERT model... (This may take a moment)")
#         tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
#         model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
#         self.nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
#         print("FinBERT model initialized.")

#     def analyze(self, text: str) -> dict:
#         """Analyzes text using the loaded FinBERT model."""
#         results = self.nlp([text])
#         return results[0] # Returns {'label': 'positive', 'score': 0.9...}

# --- Main Analysis Function ---


def analyze_dataframe(df: pd.DataFrame, model_type: str = 'vader') -> pd.DataFrame:
    """
    Applies preprocessing and sentiment analysis to a DataFrame.

    Args:
        df (pd.DataFrame): DataFrame with a 'text' column.
        model_type (str): The model to use ('vader' or 'finbert').

    Returns:
        pd.DataFrame: The original DataFrame with added 'processed_text', 
                      'sentiment_score', and 'sentiment_label' columns.
    """
    if df.empty or 'text' not in df.columns:
        return df

    df['processed_text'] = df['text'].apply(preprocess_text)
    df.dropna(subset=['processed_text'], inplace=True)

    print(f"Analyzing sentiment using {model_type}...")

    if model_type == 'vader':
        df['sentiment_score'] = df['processed_text'].apply(
            analyze_sentiment_vader)
        df['sentiment_label'] = df['sentiment_score'].apply(
            lambda c: 'positive' if c > 0.05 else ('negative' if c < -0.05 else 'neutral'))
    # elif model_type == 'finbert':
    #     # For performance, initialize the model once
    #     finbert = FinbertAnalyzer()
    #     # Note: This is slow. Analyzing one-by-one is not optimal for transformers.
    #     # For production, you would batch process the texts.
    #     finbert_results = df['processed_text'].apply(finbert.analyze)
    #     df['sentiment_label'] = finbert_results.apply(lambda x: x['label'])
    #     df['sentiment_score'] = finbert_results.apply(lambda x: x['score'] if x['label'] == 'positive' else -x['score'] if x['label'] == 'negative' else 0)
    else:
        raise ValueError(
            "Invalid model_type specified. Choose 'vader' or 'finbert'.")

    return df
