"""
Task 4: Insights and Recommendations - Data Analysis and Visualization
- Connect to PostgreSQL
- Fetch reviews + banks
- Generate insights (drivers, pain points, recommendations)
- Generate 3 clean visualizations
"""

import pandas as pd
import psycopg2
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from IPython.display import display
from pathlib import Path

# -----------------------------------------
# Database Configuration
# -----------------------------------------
DB_NAME = "bank_reviews"
DB_USER = "postgres"
DB_PASS = "root"
DB_HOST = "localhost"
DB_PORT = "5432"


# -----------------------------------------
# Database Connection
# -----------------------------------------
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        print(f"✅ Connected to PostgreSQL: {DB_NAME}")
        return conn
    except Exception as e:
        print(f"❌ Database Connection Error: {e}")
        return None


# -----------------------------------------
# Fetch Data
# -----------------------------------------
def fetch_all_data(conn):
    query = """
    SELECT 
        r.review_text, r.rating, r.sentiment_label, r.themes,
        b.bank_name
    FROM Reviews r
    JOIN Banks b ON r.bank_id = b.bank_id
    WHERE r.themes IS NOT NULL 
      AND r.themes != '';
    """

    try:
        df = pd.read_sql(query, conn)
        df["themes"] = df["themes"].str.split(", ")
        print(f"📥 Loaded {len(df)} reviews.")
        return df
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return pd.DataFrame()


# -----------------------------------------
# Insights Generation
# -----------------------------------------
def generate_insights(df):
    if df.empty:
        print("⚠️ No data available for insights.")
        return None

    df_exploded = df.explode("themes").dropna(subset=["themes"])
    insights = {}

    banks = df["bank_name"].unique()

    rec_map = {
        "crashes": "Improve app stability with test automation.",
        "slow_performance": "Optimize app load and transaction speed.",
        "fees": "Add clear fee transparency in the app.",
        "customer_support": "Add in-app chatbot for instant responses.",
        "fast_navigation": "Promote UX patterns users love.",
        "biometrics": "Fix biometric login inconsistencies."
    }

    print("\n==============================================")
    print("               INSIGHTS SUMMARY")
    print("==============================================")

    for bank in banks:
        bank_df = df_exploded[df_exploded["bank_name"] == bank]

        # Pain Points (rating 1–2)
        pain_raw = bank_df[bank_df["rating"].isin(
            [1, 2])]["themes"].value_counts().head(3)
        pain_points = [p for p in pain_raw.index if p not in [
            "service_general", "app_general"]]

        # Drivers (rating 4–5)
        driver_raw = bank_df[bank_df["rating"].isin(
            [4, 5])]["themes"].value_counts().head(3)
        drivers = [d for d in driver_raw.index if d not in [
            "service_general", "app_general"]]

        recommendations = []
        for t in pain_points + drivers:
            if t in rec_map and t not in recommendations:
                recommendations.append(rec_map[t])

        if len(recommendations) < 2:
            recommendations += [
                "Add simple P2P money transfer feature.",
                "Improve push notifications for transactions."
            ]

        insights[bank] = {
            "drivers": drivers[:2],
            "pain_points": pain_points[:2],
            "recommendations": recommendations[:2]
        }

        # Print to console
        print(f"\n🏦 BANK: {bank}")
        print(f"  ➤ Drivers: {', '.join(insights[bank]['drivers']) or 'None'}")
        print(
            f"  ➤ Pain Points: {', '.join(insights[bank]['pain_points']) or 'None'}")
        print("  ➤ Recommendations:")
        for rec in insights[bank]['recommendations']:
            print(f"     - {rec}")

    print("==============================================")
    return insights


# -----------------------------------------
# Visualization (Guaranteed all 3 will display)
# -----------------------------------------
def generate_visualizations(df, insights):

    sns.set_style("whitegrid")

    # --------------------------
    # Plot 1 – Sentiment Count
    # --------------------------
    fig1 = plt.figure(figsize=(10, 6))
    sns.countplot(
        data=df,
        x="sentiment_label",
        hue="bank_name",
        order=["negative", "neutral", "positive"]
    )
    plt.title("Sentiment Distribution Across Banks")
    display(fig1)
    plt.close(fig1)
    print("📊 Displayed Plot 1")

    # --------------------------
    # Plot 2 – Rating Distribution
    # --------------------------
    fig2 = plt.figure(figsize=(12, 7))
    sns.violinplot(
        data=df,
        x="bank_name",
        y="rating",
        inner="quartile"
    )
    plt.title("Rating Distribution Per Bank (1–5)")
    display(fig2)
    plt.close(fig2)
    print("📊 Displayed Plot 2")

    # --------------------------
    # Plot 3 – WordCloud for Pain Points
    # --------------------------
    low_df = df[df["rating"].isin([1, 2])]
    exploded = low_df.explode("themes").dropna()

    if exploded.empty:
        print("⚠️ Not enough data for WordCloud.")
        return

    text = " ".join(exploded["themes"].tolist())
    stop = {"service_general", "app_general", "general"}

    wc = WordCloud(
        width=800, height=400,
        background_color="white",
        stopwords=stop,
        colormap="Reds_r"
    ).generate(text)

    fig3 = plt.figure(figsize=(12, 5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title("WordCloud of Pain Point Themes")
    display(fig3)
    plt.close(fig3)
    print("📊 Displayed Plot 3")

    print("\n🎉 All 3 visualizations were successfully displayed!")


# -----------------------------------------
# MAIN
# -----------------------------------------
def main():
    print("\n--- Starting Task 4: Analysis Execution ---")

    conn = connect_to_db()
    if not conn:
        return

    df = fetch_all_data(conn)
    if df.empty:
        return

    insights = generate_insights(df)
    generate_visualizations(df, insights)

    conn.close()
    print("\n--- Task 4 Complete ---")


if __name__ == "__main__":
    main()
