Fintech CX Analytics

A project for analyzing user behavior, experience, and customer journey metrics in fintech applications.

🚀 Features

User behavior analytics

Churn prediction (later)

Funnel analysis

Customer segmentation

Interactive dashboards

📁 Project Structure

fintech-customer-analytics-ml/
│
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   └── eda.ipynb
├── src/
│   ├── preprocessing/
│   ├── analytics/
│   └── models/
├── reports/
│   └── figures/
├── .github/workflows/
├── .vscode/
├── .gitignore
├── requirements.txt
└── README.md

🛠 Setup

py -3.11 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt


✅ Task Deliverables

Task 1: Data Collection and Preprocessing

Scrape reviews from the Google Play Store, preprocess them for analysis, and manage code via GitHub.

Tasks

Git Setup

Create a GitHub repository.

Include .gitignore, requirements.txt.

Use “task-1” branch.

Commit frequently with meaningful messages after completing logical chunks.

Web Scraping

Use google-play-scraper to collect reviews, ratings, dates, and app names for three banks.

Target 400+ reviews per bank (1,200 total).

Preprocessing

Remove duplicates, handle missing data.

Normalize dates (e.g., YYYY-MM-DD).

Save final CSV with columns: review, rating, date, bank, source.

KPIs

1,200+ reviews collected with <5% missing data.

Clean CSV dataset produced.

Organized Git repo with clear commits.

Minimum Essential

Scrape at least 400 reviews per bank.

Commit a preprocessing script.

Update README.md with methodology.

Task 2: Sentiment and Thematic Analysis

Quantify review sentiment and identify themes to uncover satisfaction drivers and pain points.

Tasks

Sentiment Analysis

Use distilbert-base-uncased-finetuned-sst-2-english for sentiment scoring.

Optionally compare with VADER or TextBlob.

Aggregate results by bank and rating.

Thematic Analysis

A theme is a recurring concept or topic in user reviews.

Keyword Extraction & Clustering

Extract keywords and n-grams using TF-IDF or spaCy.

Optionally use topic modeling for clustering.

Group related keywords into 3–5 core themes per bank (e.g., UI/UX, Login Issues, Performance, Support, Feature Requests).

Document grouping logic.

Pipeline

Preprocessing using tokenization, stop-word removal, lemmatization if helpful.

Save results as CSV (review_id, review_text, sentiment_label, sentiment_score, identified_theme).

Implement keyword extraction.

Cluster into themes.

Git Workflow

Use “task-2” branch.

Commit scripts and merge using pull requests.

KPIs

Sentiment scores for 90%+ of reviews.

3+ themes per bank with supporting examples.

Modular pipeline code.

Minimum Essential

Sentiment for 400+ reviews.

At least 2 themes per bank.

Commit full analysis script.

Task 3: Database Integration and Data Modeling

Design and implement a relational database schema (PostgreSQL) to store structured review data and support analytics queries.

Tasks

Database Design

Design a relational schema including tables for Banks, Reviews, and any necessary lookup/join tables.

Define appropriate data types, primary keys, and foreign keys (e.g., bank_id).

ETL Script

Create a Python script using psycopg2 or similar to connect to PostgreSQL.

Implement the ETL process: Load the clean CSV from Task 2 into the database.

Ensure data integrity and correct type casting during insertion.

Data Verification

Write a SQL script to query and confirm that the data (including sentiment and themes) was loaded correctly.

Git Workflow

Use “task-3” branch.

Commit database schema and ETL scripts.

KPIs

Functional PostgreSQL database with tables normalized to at least 2NF.

All data loaded successfully, matching CSV counts.

Clean, parameterized Python ETL script.

Minimum Essential

Two tables (Banks, Reviews) connected by a foreign key.

Successful data load confirmed by a simple SQL query.

Task 4: Insights and Recommendations

Utilize the structured data in PostgreSQL to derive actionable business insights and create compelling visualizations.

Tasks

Database Querying

Connect to the PostgreSQL database from a Python analysis script.

Query and join Reviews and Banks data to aggregate sentiment, rating, and theme data per bank.

Insight Generation

Identify the top 3 drivers of satisfaction (themes associated with high ratings/positive sentiment).

Identify the top 3 pain points (themes associated with low ratings/negative sentiment).

Provide 2 actionable, concrete recommendations for each bank based on the derived pain points and drivers.

Data Visualization

Generate and display 3 distinct visualizations using Matplotlib/Seaborn:

Sentiment Distribution Bar Chart: Comparison of positive/neutral/negative review counts across all three banks.

Rating Distribution Plot: A violin or box plot showing the distribution of user ratings (1-5) for each bank.

Theme Cloud: A word cloud of themes/keywords strongly associated with low ratings (1 or 2) across all banks, highlighting critical pain points.

Git Workflow

Use “task-4” branch.

Commit the final analysis and visualization script.

KPIs

Structured insights summary printed to console/report.

3 high-quality visualizations generated and displayed.

Clear distinction between drivers and pain points.

Minimum Essential

Successful execution of the analysis script showing database connection, insights summary, and the 3 required plots (Sentiment Bar, Rating Distribution, Theme Cloud).
