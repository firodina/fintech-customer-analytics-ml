"""
Data Preprocessing Script
Task 1: Data Preprocessing

This script cleans and preprocesses the scraped reviews data.
- Handles missing values
- Normalizes dates
- Cleans text data
- Extracts detailed date features
- Generates simple data quality dashboard
"""


import pandas as pd
import numpy as np
import re
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from Script.config import DATA_PATHS
import sys
import os

# Add project root to path (one level up from src/)
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..')))


class ReviewPreprocessor:
    """Preprocessor class for review data"""

    def __init__(self, input_path=None, output_path=None):
        self.input_path = input_path or DATA_PATHS['raw_reviews']
        self.output_path = output_path or DATA_PATHS['processed_reviews']
        self.df = None
        self.stats = {}

    def load_data(self):
        print("Loading raw data...")
        try:
            self.df = pd.read_csv(self.input_path)
            print(f"Loaded {len(self.df)} reviews")
            self.stats['original_count'] = len(self.df)
            return True
        except Exception as e:
            print(f"ERROR: Failed to load data: {e}")
            return False

    def check_missing_data(self):
        print("\n[1/6] Checking for missing data...")
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df)) * 100
        for col in missing.index:
            if missing[col] > 0:
                print(f"  {col}: {missing[col]} ({missing_pct[col]:.2f}%)")

    def handle_missing_values(self):
        print("\n[2/6] Handling missing values...")
        critical_cols = ['review_text', 'rating', 'bank_name']
        before_count = len(self.df)
        self.df = self.df.dropna(subset=critical_cols)
        removed = before_count - len(self.df)
        print(f"Removed {removed} rows with missing critical values")

        self.df['user_name'] = self.df.get(
            'user_name', pd.Series()).fillna('Anonymous')
        self.df['thumbs_up'] = self.df.get('thumbs_up', pd.Series()).fillna(0)
        self.df['reply_content'] = self.df.get(
            'reply_content', pd.Series()).fillna('')

        self.stats['rows_removed_missing'] = removed
        self.stats['count_after_missing'] = len(self.df)

    def normalize_dates(self):
        print("\n[3/6] Normalizing dates...")
        self.df['review_date'] = pd.to_datetime(
            self.df['review_date'], errors='coerce')
        self.df.dropna(subset=['review_date'], inplace=True)

        # Extract full date features
        self.df['review_date_only'] = self.df['review_date'].dt.date
        self.df['review_year'] = self.df['review_date'].dt.year
        self.df['review_month'] = self.df['review_date'].dt.month
        self.df['review_day'] = self.df['review_date'].dt.day
        self.df['review_weekday'] = self.df['review_date'].dt.day_name()

        print(
            f"Date range: {self.df['review_date_only'].min()} to {self.df['review_date_only'].max()}")

    def clean_text(self):
        print("\n[4/6] Cleaning text...")

        def clean_review(text):
            if pd.isna(text):
                return ''
            text = str(text)
            text = re.sub(r'\s+', ' ', text).strip()
            return text

        self.df['review_text'] = self.df['review_text'].apply(clean_review)
        before_count = len(self.df)
        self.df = self.df[self.df['review_text'].str.len() > 0]
        removed = before_count - len(self.df)
        print(f"Removed {removed} reviews with empty text")

        self.df['text_length'] = self.df['review_text'].str.len()
        self.stats['empty_reviews_removed'] = removed
        self.stats['count_after_cleaning'] = len(self.df)

    def validate_ratings(self):
        print("\n[5/6] Validating ratings...")
        invalid = self.df[(self.df['rating'] < 1) | (self.df['rating'] > 5)]
        if len(invalid) > 0:
            print(
                f"WARNING: Found {len(invalid)} invalid ratings. Removing them...")
            self.df = self.df[(self.df['rating'] >= 1) &
                              (self.df['rating'] <= 5)]
        else:
            print("All ratings are valid (1-5)")
        self.stats['invalid_ratings_removed'] = len(invalid)

    def prepare_final_output(self):
        print("\n[6/6] Preparing final output...")
        output_columns = [
            'review_id', 'review_text', 'rating', 'review_date', 'review_year', 'review_month',
            'review_day', 'review_weekday', 'bank_code', 'bank_name', 'user_name',
            'thumbs_up', 'text_length', 'source'
        ]
        output_columns = [c for c in output_columns if c in self.df.columns]
        self.df = self.df[output_columns]
        self.df = self.df.sort_values(
            ['bank_code', 'review_date'], ascending=[True, False])
        self.df = self.df.reset_index(drop=True)
        print(f"Final dataset: {len(self.df)} reviews")

    def save_data(self):
        print("\nSaving processed data...")
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        self.df.to_csv(self.output_path, index=False)
        print(f"Data saved to: {self.output_path}")
        self.stats['final_count'] = len(self.df)

    def generate_dashboard(self):
        print("\nGenerating simple dashboard...")
        # Missing values heatmap
        plt.figure(figsize=(10, 6))
        sns.heatmap(self.df.isna(), cbar=False)
        plt.title("Missing Values Heatmap")
        plt.tight_layout()
        plt.savefig("missing_values_heatmap.png")

        # Rating distribution
        plt.figure(figsize=(6, 4))
        self.df['rating'].value_counts().sort_index().plot(
            kind='bar', color='skyblue')
        plt.title("Rating Distribution")
        plt.tight_layout()
        plt.savefig("rating_distribution.png")

        # Monthly review counts
        plt.figure(figsize=(8, 4))
        monthly_counts = self.df.groupby(
            ['review_year', 'review_month']).size().reset_index(name='count')
        monthly_counts['month_year'] = monthly_counts['review_year'].astype(
            str) + "-" + monthly_counts['review_month'].astype(str)
        sns.barplot(x='month_year', y='count',
                    data=monthly_counts, color='lightgreen')
        plt.xticks(rotation=45)
        plt.title("Monthly Review Counts")
        plt.tight_layout()
        plt.savefig("monthly_review_counts.png")

    def process(self):
        if not self.load_data():
            return False
        self.check_missing_data()
        self.handle_missing_values()
        self.normalize_dates()
        self.clean_text()
        self.validate_ratings()
        self.prepare_final_output()
        self.save_data()
        self.generate_dashboard()
        return True


def main():
    preprocessor = ReviewPreprocessor()
    success = preprocessor.process()
    if success:
        print("\n✓ Preprocessing completed successfully!")
        return preprocessor.df
    else:
        print("\n✗ Preprocessing failed!")
        return None


if __name__ == "__main__":
    processed_df = main()
