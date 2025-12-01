# 02_keywords_topics.py
"""
Compute TF-IDF top n-grams per bank and build an LDA model (optional)
to surface topics to help theme grouping.
"""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from utils import OUTPUT_DIR, load_reviews


def top_tfidf_per_bank(df, ngram_range=(1, 2), top_n=30):
    # FIX: Change 'bank' to 'bank_name'
    banks = df["bank_name"].unique()
    results = []
    for b in banks:
        # FIX: Change 'bank' to 'bank_name'
        sub = df[df["bank_name"] == b]

        corpus = sub["cleaned_review"].fillna("").tolist()

        # ... rest of the TF-IDF logic ...
        vec = TfidfVectorizer(ngram_range=ngram_range, max_features=5000)
        tfidf = vec.fit_transform(corpus)
        sums = tfidf.sum(axis=0).A1
        terms = vec.get_feature_names_out()
        top_idx = sums.argsort()[::-1][:top_n]
        top_terms = [(terms[i], float(sums[i])) for i in top_idx]

        # Keep the key as 'bank' in the output JSON for simplicity
        results.append({"bank": b, "top_terms": top_terms})
    return results


def lda_topics(df, n_topics=8):
    # UPDATED: Use 'cleaned_review' column
    corpus = df["cleaned_review"].fillna("").tolist()

    cv = CountVectorizer(max_df=0.95, min_df=5, ngram_range=(1, 2))
    dtm = cv.fit_transform(corpus)

    # LDA model visualization (optional but helpful)
    #

    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(dtm)
    terms = cv.get_feature_names_out()
    topics = []
    for i, comp in enumerate(lda.components_):
        terms_idx = comp.argsort()[::-1][:15]
        topics.append([terms[t] for t in terms_idx])
    return topics


# 02_keywords_topics.py

# ... (imports and functions remain the same) ...

def main():
    # 1. Load the original dataframe (which contains the 'bank' column)
    print("Loading base data to get 'bank' column...")
    df_base = load_reviews()  # This should load the file with 'bank' and original IDs/Text

    # 2. Load the cleaned reviews file (which contains 'cleaned_review')
    CLEANED_FILE = OUTPUT_DIR / "reviews_cleaned.csv"

    if not CLEANED_FILE.exists():
        raise FileNotFoundError(
            f"Expected file not found at {CLEANED_FILE}. "
            "Please ensure you run the previous script (00_preprocess.py) first."
        )

    df_cleaned = pd.read_csv(CLEANED_FILE)
    print(f"Loaded {len(df_cleaned)} rows of cleaned data.")

    # 3. Merge the cleaned text onto the base dataframe.
    #    We assume the two dataframes align by index or implicit ID.
    #    A safer way is to ensure a common ID column, but based on the project structure,
    #    we'll assume the rows are in the same order and merge the columns.

    # Check if 'cleaned_review' is already in df_base (if 00_preprocess saved all columns)
    if 'cleaned_review' not in df_base.columns:
        # Assuming the rows align, merge the cleaned column
        df_base['cleaned_review'] = df_cleaned['cleaned_review']
        df_pre = df_base[df_base['cleaned_review'].notna()]
    else:
        df_pre = df_base  # Use df_base if 00_preprocess saved everything

    # Sanity check for the column required by the functions
    if 'cleaned_review' not in df_pre.columns:
        raise KeyError(
            "Could not find the 'cleaned_review' column after loading/merging.")

    print("Computing TF-IDF keywords per bank...")
    tfidf = top_tfidf_per_bank(df_pre)

    import json
    with open(OUTPUT_DIR / "tfidf_top_terms.json", "w") as f:
        json.dump(tfidf, f, indent=2)

    print("Running LDA for topic modeling...")
    topics = lda_topics(df_pre, n_topics=8)
    with open(OUTPUT_DIR / "lda_topics.json", "w") as f:
        json.dump(topics, f, indent=2)

    print("✅ Saved tf-idf and lda outputs to outputs/ folder.")


if __name__ == "__main__":
    # Ensure the code above is placed *inside* the 02_keywords_topics.py file
    main()
    # FIX 1: Change filename from 'reviews_preprocessed.csv' to 'reviews_cleaned.csv'
    CLEANED_FILE = OUTPUT_DIR / "reviews_cleaned.csv"

    if not CLEANED_FILE.exists():
        raise FileNotFoundError(
            f"Expected file not found at {CLEANED_FILE}. "
            "Please ensure you run the previous script (00_preprocess.py) first."
        )

    # Load the cleaned data
    df_pre = pd.read_csv(CLEANED_FILE)
    print(f"Loaded {len(df_pre)} rows of cleaned data.")

    # You still need bank info, so load the original dataframe too if not merged in df_pre
    # Assuming 'bank' column is preserved in reviews_cleaned.csv

    print("Computing TF-IDF keywords per bank...")
    tfidf = top_tfidf_per_bank(df_pre)

    import json
    with open(OUTPUT_DIR / "tfidf_top_terms.json", "w") as f:
        json.dump(tfidf, f, indent=2)

    print("Running LDA for topic modeling...")
    topics = lda_topics(df_pre, n_topics=8)
    with open(OUTPUT_DIR / "lda_topics.json", "w") as f:
        json.dump(topics, f, indent=2)

    print("✅ Saved tf-idf and lda outputs to outputs/ folder.")


if __name__ == "__main__":
    main()
