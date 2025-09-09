import pandas as pd
import feedparser
from datetime import datetime
import pytz
import config


def parse_feed_entry(entry, source_name: str) -> dict:
    """Parses a single entry from an RSS feed and returns a structured dictionary."""
    # Try to get the published date, fall back to the updated date
    try:
        published_time = entry.get(
            'published_parsed', entry.get('updated_parsed'))
        timestamp = datetime.fromtimestamp(
            # mktime is not available in time module, use calendar.timegm if needed
            # For now, let's assume direct conversion works if struct_time is correct
            pd.to_datetime(published_time).timestamp()
        ).astimezone(pytz.utc)
    except Exception:
        timestamp = datetime.now(pytz.utc)

    return {
        'timestamp': timestamp,
        'text': entry.get('title', 'No Title'),
        'source': source_name
    }


def get_data(ticker: str, num_headlines: int = 50) -> pd.DataFrame:
    """
    Fetches news headlines for a given ticker from multiple RSS feeds defined in config.
    """
    all_headlines = []
    print(
        f"Fetching data for {ticker} from {len(config.RSS_FEEDS)} sources...")

    for source_name, feed_url_template in config.RSS_FEEDS.items():
        feed_url = feed_url_template.format(ticker=ticker)
        try:
            feed = feedparser.parse(feed_url)

            # Check if feed has entries
            if feed.entries:
                print(
                    f"  - Found {len(feed.entries)} headlines from {source_name}")
                for entry in feed.entries:
                    parsed_entry = parse_feed_entry(entry, source_name)
                    all_headlines.append(parsed_entry)
            else:
                print(f"  - No entries found from {source_name}")

        except Exception as e:
            print(
                f"  - Could not fetch or parse feed from {source_name}. Error: {e}")

    if not all_headlines:
        print(
            f"Warning: No headlines were found for {ticker} from any source.")
        return pd.DataFrame()

    # Create DataFrame and limit to the requested number of headlines
    df = pd.DataFrame(all_headlines)
    df = df.sort_values(by='timestamp', ascending=False).head(num_headlines)

    print(f"Total unique headlines collected for {ticker}: {len(df)}")
    return df
