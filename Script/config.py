"""
Configuration file for Bank Reviews Analysis Project
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Google Play Store App IDs
APP_IDS = {
    'CBE': os.getenv('CBE_APP_ID', 'com.combanketh.mobilebanking'),
    'Dashen Bank': os.getenv('Dashen_Bank_APP_ID', 'com.dashen.dashensuperapp'),
    'Abyssinia Bank': os.getenv('Abyssinia_Bank_APP_ID', 'com.boa.boaMobileBanking')
}

# Bank Names Mapping
BANK_NAMES = {
    'CBE': 'Commercial Bank of Ethiopia',
    'Dashen Bank': 'Dashen Bank',
    'Abyssinia Bank': 'Abyssinia Bank'
}


# Scraping configuration
SCRAPING_CONFIG = {
    'reviews_per_bank': int(os.getenv('REVIEWS_PER_BANK', 400)),
    'max_retries': int(os.getenv('MAX_RETRIES', 3)),
    'lang': 'en',
    'country': 'et'
}

# File paths
DATA_PATHS = {
    'raw': 'data/raw',
    'processed': 'data/processed',
    'raw_reviews': 'data/raw/reviews_raw.csv',
    'processed_reviews': 'data/processed/reviews_processed.csv',
    'app_info': 'data/raw/app_info.csv'
}
