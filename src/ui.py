import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import config
from data_acquisition import get_data
from sentiment_analysis import analyze_dataframe
from database import save_sentiments

# --- Page Configuration ---
st.set_page_config(
    page_title="Stock Sentiment Dashboard",
    page_icon="💹",
    layout="wide"
)

# --- Helper Functions ---


@st.cache_data(ttl=300)  # Cache data for 5 minutes
def load_data_from_db(db_file: str) -> pd.DataFrame:
    """Connects to the SQLite DB and loads all sentiment data into a DataFrame."""
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)
        df = pd.read_sql_query("SELECT * FROM sentiments", conn)
        conn.close()
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except Exception:
        # Return empty dataframe if table doesn't exist yet
        return pd.DataFrame()


def run_analysis_for_ticker(ticker: str):
    """Triggers the data pipeline for a specific ticker and saves results to the DB."""
    with st.spinner(f"Fetching and analyzing new data for ${ticker}... This may take a moment."):
        raw_data_df = get_data(
            ticker=ticker, num_headlines=config.NUM_HEADLINES)
        if not raw_data_df.empty:
            analyzed_df = analyze_dataframe(
                df=raw_data_df, model_type=config.ANALYSIS_MODEL)
            save_sentiments(df=analyzed_df, ticker=ticker,
                            db_file=config.DB_FILE)
            st.success(f"Analysis complete for ${ticker}!")
            # Clear the cache to force a reload from the DB on the next run
            st.cache_data.clear()
        else:
            st.warning(
                f"Could not find any news headlines for ${ticker}. Please check the ticker symbol.")


def get_overall_sentiment_label(score: float) -> str:
    """Converts a sentiment score into a qualitative label."""
    # This threshold can be adjusted to be more or less sensitive
    threshold = 0.05

    if score > threshold:
        return "Bullish"
    elif score < -threshold:
        return "Bearish"
    else:
        return "Neutral"


# --- Main Application UI ---
st.title("📰 On-Demand Stock News Sentiment Analysis")

# Load data using the cached function
main_df = load_data_from_db(config.DB_FILE)

# --- Sidebar for Controls ---
st.sidebar.header("Controls")

# Use session state to remember the last analyzed ticker
if 'last_ticker' not in st.session_state:
    st.session_state.last_ticker = config.TICKERS[0] if config.TICKERS else "AAPL"

# Text input for the ticker search
search_ticker = st.sidebar.text_input(
    "Enter a Ticker Symbol",
    value=st.session_state.last_ticker
).upper()

# Button to trigger the analysis
if st.sidebar.button("Run Analysis"):
    if search_ticker:
        st.session_state.last_ticker = search_ticker
        run_analysis_for_ticker(search_ticker)
        # Rerun the app to see the changes immediately
        st.rerun()
    else:
        st.sidebar.error("Please enter a ticker symbol.")

st.sidebar.info("Click 'Run Analysis' to get the latest sentiment on a ticker. The backend data collector (`main.py`) can still be run to pre-populate the database.")

# --- Main Dashboard Display ---
selected_ticker = st.session_state.last_ticker
st.header(f"Sentiment Analysis for ${selected_ticker}")

if main_df.empty:
    st.warning("No data found. Enter a ticker and click 'Run Analysis' to begin.")
else:
    df_filtered = main_df[main_df['ticker'] == selected_ticker]

    if df_filtered.empty:
        st.warning(
            f"No data is available for '{selected_ticker}'. Please run the analysis for this ticker.")
    else:
        # --- Key Metrics Display ---
        st.subheader("Overall Sentiment")
        avg_sentiment = df_filtered['sentiment_score'].mean()
        overall_label = get_overall_sentiment_label(avg_sentiment)
        total_headlines = len(df_filtered)

        # Display the qualitative label, the score, and the headline count
        col1, col2, col3 = st.columns(3)
        col1.metric("Overall Sentiment", overall_label)
        col2.metric("Average Score", f"{avg_sentiment:.3f}")
        col3.metric("Headlines Analyzed", f"{total_headlines}")

        st.subheader("Headline Counts by Category")
        sentiment_counts = df_filtered['sentiment_label'].value_counts().reindex(
            ['positive', 'neutral', 'negative'], fill_value=0)

        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Positive Headlines", f"{sentiment_counts['positive']}")
        col_b.metric("Neutral Headlines", f"{sentiment_counts['neutral']}")
        col_c.metric("Negative Headlines", f"{sentiment_counts['negative']}")

        # --- Visualizations ---
        st.subheader("Visualizations")
        col_viz1, col_viz2 = st.columns(2)

        with col_viz1:
            fig_pie = px.pie(
                df_filtered,
                names='sentiment_label',
                title='Sentiment Distribution',
                color='sentiment_label',
                color_discrete_map={'positive': '#2ca02c',
                                    'negative': '#d62728', 'neutral': '#7f7f7f'}
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with col_viz2:
            df_resampled = df_filtered.set_index('timestamp').resample(
                'H').mean(numeric_only=True).dropna().reset_index()
            fig_line = px.line(
                df_resampled,
                x='timestamp',
                y='sentiment_score',
                title='Sentiment Trend (Hourly Average)',
                markers=True
            )
            fig_line.update_layout(yaxis_title="Average Sentiment Score")
            st.plotly_chart(fig_line, use_container_width=True)

        # --- Data Table of Recent Headlines ---
        st.subheader("Analyzed Headlines")
        st.dataframe(
            df_filtered[['timestamp', 'source', 'text', 'sentiment_label', 'sentiment_score']].sort_values(
                'timestamp', ascending=False
            ).reset_index(drop=True)
        )
