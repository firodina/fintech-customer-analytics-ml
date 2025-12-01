# src/task-2/_00_preprocess.py

import re
import pandas as pd
import nltk
from pathlib import Path
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from utils import PROJECT_ROOT, load_reviews

# -------------------------------
# 1️⃣ Setup NLTK safely (works in Jupyter / venv)
# -------------------------------
nltk_data_dir = Path.home() / "nltk_data"
nltk_data_dir.mkdir(exist_ok=True)

# Ensure NLTK uses this path
if str(nltk_data_dir) not in nltk.data.path:
    nltk.data.path.append(str(nltk_data_dir))

# Download necessary packages if missing
# UPDATED: Added "punkt_tab" and "omw-1.4" to fix LookupError
needed_packages = ["stopwords", "punkt", "punkt_tab", "wordnet", "omw-1.4"]

for package in needed_packages:
    try:
        if package in ["punkt", "punkt_tab"]:
            nltk.data.find(f"tokenizers/{package}")
        else:
            nltk.data.find(f"corpora/{package}")
    except LookupError:
        print(f"Downloading missing NLTK package: {package}...")
        nltk.download(package, download_dir=str(nltk_data_dir))

# -------------------------------
# 2️⃣ Text preprocessing function
# -------------------------------


def preprocess_text(text):
    if not isinstance(text, str):
        return ""

    # 1. Lowercase
    text = text.lower()

    # 2. Remove special characters, numbers, emojis, and punctuation
    #    Keep only letters (a-z) and whitespace (\s)
    text = re.sub(r'[^a-z\s]', '', text)

    # 3. Tokenize
    tokens = word_tokenize(text)

    # 4. Remove stopwords
    stop_words = set(stopwords.words("english"))
    tokens = [t for t in tokens if t not in stop_words]

    # 5. Lemmatize
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(t) for t in tokens]

    return " ".join(tokens)

# -------------------------------
# 3️⃣ Main preprocessing routine
# -------------------------------


def main():
    # Load reviews CSV
    print("Loading data...")
    df = load_reviews()  # Automatically finds reviews_processed.csv

    # Auto-detect review column by name & longest average string length
    candidate_cols = [col for col in df.columns if "review" in col.lower()]
    if not candidate_cols:
        raise ValueError(
            f"No column containing 'review' found. Columns: {df.columns.tolist()}")

    avg_lengths = {col: df[col].dropna().astype(str).map(len).mean()
                   for col in candidate_cols}
    review_column = max(avg_lengths, key=avg_lengths.get)

    print(
        f"Auto-selected review column: '{review_column}' (avg length {avg_lengths[review_column]:.1f})")

    # Preprocess text
    print("Preprocessing text (cleaning, tokenizing, lemmatizing)...")
    df["cleaned_review"] = df[review_column].apply(preprocess_text)

    # Save to output directory
    OUTPUT_DIR = PROJECT_ROOT / "data" / "outputs"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / "reviews_cleaned.csv"

    df.to_csv(output_file, index=False)
    print(f"✅ Success! Saved cleaned reviews to {output_file}")


# -------------------------------
# 4️⃣ Run main
# -------------------------------
if __name__ == "__main__":
    main()
