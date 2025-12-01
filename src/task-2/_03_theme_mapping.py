# 03_theme_mapping.py
"""
Rule-based mapping of keywords to themes.
This file provides:
- a dictionary of theme -> keyword patterns
- a function to label each review with 0/1 theme membership
"""
import pandas as pd
import re
from utils import OUTPUT_DIR

# --- Theme Definitions (No change needed here) ---
THEME_KEYWORDS = {
    "Account Access": ["login", "otp", "password", "pin", "locked account", "two factor", "two-factor", "sign in", "signin"],
    "Transactions": ["transfer failed", "transfer", "payment failed", "pending", "transaction failed", "send money", "receive", "failed payment"],
    "App Stability": ["crash", "crashed", "freeze", "bug", "force close", "force-close", "hang"],
    "UI / UX": ["ui", "ux", "design", "easy to use", "confusing", "navigation", "slow ui", "layout"],
    "Customer Support": ["support", "customer service", "call center", "agent", "response time", "reply", "help"],
    "Feature Requests": ["feature", "add", "biometric", "fingerprint", "face id", "statement", "schedule"],
}


def map_themes(text):
    labels = []
    # Ensure text is a string before lowercasing
    text_l = str(text).lower()

    for theme, kws in THEME_KEYWORDS.items():
        for kw in kws:
            # Using simple 'in' check is okay for simple strings
            if kw in text_l:
                labels.append(theme)
                break
    return ",".join(labels)


def main():
    # 1. Load the file containing sentiment results and, hopefully, the cleaned review
    FILE_PATH = OUTPUT_DIR / "sentiment_results.csv"
    if not FILE_PATH.exists():
        # Fallback to the latest successful file if sentiment_results hasn't run yet
        FILE_PATH = OUTPUT_DIR / "reviews_cleaned.csv"
        print(
            f"Warning: sentiment_results.csv not found. Using {FILE_PATH.name} instead.")

    df = pd.read_csv(FILE_PATH)

    # 2. Standardize the column name for text analysis
    TEXT_COL = "cleaned_review"

    if TEXT_COL not in df.columns:
        # If 'cleaned_review' is missing (should not happen if 00_ and 01_ ran correctly)
        raise KeyError(
            f"Required column '{TEXT_COL}' not found in the loaded data. "
            "Ensure previous steps (00_preprocess.py) were run successfully."
        )

    # 3. Apply the theme mapping function using the clean text
    df["themes"] = df[TEXT_COL].apply(map_themes)

    # 4. Save the results
    df.to_csv(OUTPUT_DIR / "sentiment_thematic.csv", index=False)
    print("✅ Saved outputs/sentiment_thematic.csv")


if __name__ == "__main__":
    main()
