# src/task-2/01_sentiment.py
"""
Two modes:
- 'transformer' uses HuggingFace model distilbert... (recommended if you can download model)
- 'vader' uses NLTK VADER as fallback (no heavy downloads)

TextBlob analysis is run alongside the selected mode to generate columns 
needed for downstream correlation visualizations.
"""
import pandas as pd
from utils import OUTPUT_DIR, load_reviews
import nltk
from pathlib import Path
from textblob import TextBlob  # New Import!

MODE = "vader"  # change to 'transformer' if available

# -------------------------------
# Ensure NLTK VADER lexicon is downloaded
# -------------------------------
nltk_data_dir = Path.home() / "nltk_data"
nltk_data_dir.mkdir(exist_ok=True)
if str(nltk_data_dir) not in nltk.data.path:
    nltk.data.path.append(str(nltk_data_dir))

try:
    nltk.data.find("sentiment/vader_lexicon.zip")
except LookupError:
    nltk.download('vader_lexicon', download_dir=str(nltk_data_dir))


def get_review_column(df):
    """Helper to find the correct column name safely."""
    if "cleaned_review" in df.columns:
        return "cleaned_review"
    elif "review_text" in df.columns:
        return "review_text"
    elif "review" in df.columns:
        return "review"
    else:
        raise KeyError(
            f"Could not find review column. Columns are: {df.columns.tolist()}")

# -------------------------------
# NEW: TextBlob Analysis Function
# -------------------------------


def textblob_sentiment(df):
    """Adds TextBlob polarity and subjectivity columns to the DataFrame."""
    col_name = get_review_column(df)

    # Get polarity and subjectivity
    df["tb_polarity"] = df[col_name].apply(
        lambda x: TextBlob(str(x)).sentiment.polarity)
    df["tb_subjectivity"] = df[col_name].apply(
        lambda x: TextBlob(str(x)).sentiment.subjectivity)

    return df

# -------------------------------
# VADER Analysis Function
# -------------------------------


def vader_sentiment(df):
    from nltk.sentiment.vader import SentimentIntensityAnalyzer

    sid = SentimentIntensityAnalyzer()

    # FIX: Get the correct column name dynamically
    col_name = get_review_column(df)
    print(f"Running VADER on column: '{col_name}'")

    df["vader_compound"] = df[col_name].apply(
        lambda x: sid.polarity_scores(str(x))["compound"])

    def label_from_compound(c):
        if c >= 0.05:
            return "positive"
        elif c <= -0.05:
            return "negative"
        else:
            return "neutral"

    df["sentiment_label"] = df["vader_compound"].apply(label_from_compound)
    df["sentiment_score"] = df["vader_compound"]
    return df


def transformer_sentiment(df):
    # requires transformers & torch, internet to download the model on first run
    from transformers import pipeline
    classifier = pipeline(
        "sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

    col_name = get_review_column(df)
    print(f"Running Transformer on column: '{col_name}'")

    def infer(text):
        try:
            # Truncate to 512 tokens to avoid errors
            r = classifier(str(text)[:512])[0]
            label = r["label"].lower()
            score = float(r["score"])
            # map LABELS: 'POSITIVE'/'NEGATIVE'
            if score < 0.6:
                # consider low-confidence as neutral
                return ("neutral", score if label == "positive" else -score)
            return (label, score if label == "positive" else -score)
        except Exception as e:
            return ("neutral", 0.0)

    out = df[col_name].apply(lambda t: infer(t))
    df["sentiment_label"] = out.apply(lambda x: x[0])
    df["sentiment_score"] = out.apply(lambda x: x[1])
    return df


def main():
    # Load the CLEANED file if possible, otherwise processed
    try:
        # Try to load the output from the previous step
        clean_path = OUTPUT_DIR / "reviews_cleaned.csv"
        if clean_path.exists():
            print(f"Loading cleaned data from {clean_path}")
            df = pd.read_csv(clean_path)
        else:
            print("Cleaned data not found, falling back to raw processed data.")
            df = load_reviews()
    except Exception as e:
        df = load_reviews()

    # 1. Run TextBlob analysis to generate tb_polarity needed for visualization
    df = textblob_sentiment(df)

    # 2. Run the selected sentiment mode (VADER or Transformer)
    if MODE == "vader":
        df = vader_sentiment(df)
    else:
        df = transformer_sentiment(df)

    output_file = OUTPUT_DIR / "sentiment_results.csv"
    df.to_csv(output_file, index=False)
    print(f"Saved sentiment_results.csv to {output_file}")

    # Basic KPI
    coverage = df["sentiment_label"].notnull().mean()
    print(f"Sentiment coverage: {coverage*100:.2f}%")
    print("✅ TextBlob and VADER scores saved, ready for correlation plots.")


if __name__ == "__main__":
    main()
