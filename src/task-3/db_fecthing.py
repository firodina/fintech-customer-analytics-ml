# db_review_utils.py
import pandas as pd
import psycopg2
from IPython.display import display

# -----------------------------
# 1️⃣ Database Configuration
# -----------------------------
DB_NAME = "bank_reviews"
DB_USER = "postgres"
DB_PASS = "root"
DB_HOST = "localhost"
DB_PORT = "5432"

# -----------------------------
# 2️⃣ Connect to PostgreSQL
# -----------------------------


def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        print("✅ Connected to PostgreSQL")
        return conn
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return None

# -----------------------------
# 3️⃣ Fetch reviews with bank names
# -----------------------------


def fetch_reviews(limit=500):
    conn = connect_to_db()
    if conn is None:
        return None

    try:
        query = f"""
        SELECT 
            r.review_id,
            r.bank_id,
            b.bank_name,
            r.review_text,
            r.rating,
            r.review_date,
            r.sentiment_label,
            r.themes,
            r.source
        FROM Reviews r
        JOIN Banks b ON r.bank_id = b.bank_id
        ORDER BY r.review_date DESC
        LIMIT {limit};
        """
        df = pd.read_sql(query, conn)
        print(f"✅ Fetched {len(df)} reviews from DB")
        return df
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return None
    finally:
        conn.close()
        print("🔒 Database connection closed")

# -----------------------------
# 4️⃣ KPI Calculations & Counts
# -----------------------------


def compute_review_kpis(df_reviews):
    if df_reviews is None or df_reviews.empty:
        print("❌ No reviews to process.")
        return

    # 1️⃣ Total Reviews
    total_reviews = len(df_reviews)
    print(f"✅ Total Reviews: {total_reviews}\n")

    # 2️⃣ Average rating & total reviews per bank
    avg_rating_df = (
        df_reviews.groupby('bank_name')
        .agg(
            average_rating=('rating', 'mean'),
            total_reviews=('review_id', 'count')
        )
        .reset_index()
    )
    avg_rating_df['average_rating'] = avg_rating_df['average_rating'].round(2)
    print("✅ Average Rating & Total Reviews per Bank:")
    display(avg_rating_df.sort_values('total_reviews', ascending=False))

    # 3️⃣ Count of positive/negative/neutral reviews per bank
    sentiment_count_df = (
        df_reviews.groupby(['bank_name', 'sentiment_label'])
        .size()
        .reset_index(name='sentiment_count')
        .sort_values(['bank_name', 'sentiment_count'], ascending=[True, False])
    )
    print("✅ Sentiment Counts per Bank:")
    display(sentiment_count_df)

# -----------------------------
# 5️⃣ Optional: Rating counts per bank
# -----------------------------


def rating_counts_per_bank(df_reviews):
    if df_reviews is None or df_reviews.empty:
        print("❌ No reviews to process.")
        return

    rating_counts = df_reviews.groupby(
        ['bank_name', 'rating']).size().reset_index(name='review_count')
    rating_counts = rating_counts.sort_values(
        ['bank_name', 'rating'], ascending=[True, False])
    print("✅ Review Counts by Bank and Rating:")
    display(rating_counts)
